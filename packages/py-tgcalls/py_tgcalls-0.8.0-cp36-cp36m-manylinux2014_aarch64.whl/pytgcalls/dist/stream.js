"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Stream = void 0;
const fs_1 = require("fs");
const events_1 = require("events");
const wrtc_1 = require("wrtc");
const binding_1 = require("./binding");
class Stream extends events_1.EventEmitter {
    constructor(filePath, bitsPerSample = 16, sampleRate = 48000, channelCount = 1, buffer_length = 10, timePulseBuffer = buffer_length == 4 ? 1.5 : 0) {
        super();
        this.filePath = filePath;
        this.bitsPerSample = bitsPerSample;
        this.sampleRate = sampleRate;
        this.channelCount = channelCount;
        this.buffer_length = buffer_length;
        this.timePulseBuffer = timePulseBuffer;
        this.paused = false;
        this.finished = true;
        this.stopped = false;
        this.finishedLoading = false;
        this.bytesLoaded = 0;
        this.playedBytes = 0;
        this.bytesSpeed = 0;
        this.lastLag = 0;
        this.equalCount = 0;
        this.lastBytesLoaded = 0;
        this.finishedBytes = false;
        this.lastByteCheck = 0;
        this.lastByte = 0;
        this.runningPulse = false;
        this.isVideo = false;
        this.videoWidth = 0;
        this.videoHeight = 0;
        this.videoFramerate = 0;
        this.lastDifferenceRemote = 0;
        this.endListener = (() => {
            this.finishedLoading = true;
            if (this.filePath !== undefined) {
                binding_1.Binding.log('COMPLETED_BUFFERING -> ' + new Date().getTime() +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
                binding_1.Binding.log('BYTES_STREAM_CACHE_LENGTH -> ' + this.cache.length +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
                binding_1.Binding.log('BYTES_LOADED -> ' +
                    this.bytesLoaded +
                    'OF -> ' +
                    Stream.getFilesizeInBytes(this.filePath) +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
            }
        }).bind(this);
        this.dataListener = ((data) => {
            this.bytesLoaded += data.length;
            this.bytesSpeed = data.length;
            try {
                if (!this.needsBuffering()) {
                    this.readable?.pause();
                    this.runningPulse = false;
                }
            }
            catch (e) {
                this.emit('stream_deleted');
                return;
            }
            this.cache = Buffer.concat([this.cache, data]);
        }).bind(this);
        this.audioSource = new wrtc_1.nonstandard.RTCAudioSource();
        this.videoSource = new wrtc_1.nonstandard.RTCVideoSource();
        this.cache = Buffer.alloc(0);
        this.paused = true;
        if (this.filePath !== undefined) {
            this.setReadable(this.filePath);
        }
        setTimeout(() => this.processData(), 1);
    }
    setReadable(filePath) {
        this.bytesLoaded = 0;
        this.bytesSpeed = 0;
        this.lastLag = 0;
        this.equalCount = 0;
        this.lastBytesLoaded = 0;
        this.finishedBytes = false;
        this.lastByteCheck = 0;
        this.lastByte = 0;
        this.playedBytes = 0;
        if (this.readable) {
            this.readable.removeListener('data', this.dataListener);
            this.readable.removeListener('end', this.endListener);
        }
        this.filePath = filePath;
        if (filePath === undefined) {
            this.readable = undefined;
            return;
        }
        this.readable = (0, fs_1.createReadStream)(filePath);
        if (this.stopped) {
            throw new Error('Cannot set readable when stopped');
        }
        this.cache = Buffer.alloc(0);
        if (this.readable !== undefined) {
            this.finished = false;
            this.finishedLoading = false;
            this.readable.on('data', this.dataListener);
            this.readable.on('end', this.endListener);
        }
    }
    static getFilesizeInBytes(path) {
        return (0, fs_1.statSync)(path).size;
    }
    needed_time() {
        return this.isVideo ? 0.5 : 50;
    }
    needsBuffering(withPulseCheck = true) {
        if (this.finishedLoading || this.filePath === undefined) {
            return false;
        }
        let result = this.cache.length < this.bytesLength() * this.needed_time() * this.buffer_length;
        result =
            result &&
                (this.bytesLoaded <
                    Stream.getFilesizeInBytes(this.filePath) -
                        this.bytesSpeed * 2 ||
                    this.finishedBytes);
        if (this.timePulseBuffer > 0 && withPulseCheck) {
            result = result && this.runningPulse;
        }
        return result;
    }
    checkLag() {
        if (this.finishedLoading) {
            return false;
        }
        return this.cache.length < this.bytesLength() * this.needed_time();
    }
    pause() {
        if (this.stopped) {
            throw new Error('Cannot pause when stopped');
        }
        this.paused = true;
        this.emit('pause', this.paused);
    }
    resume() {
        if (this.stopped) {
            throw new Error('Cannot resume when stopped');
        }
        this.paused = false;
        this.emit('resume', this.paused);
    }
    finish() {
        this.finished = true;
    }
    stop() {
        this.finish();
        this.stopped = true;
    }
    createAudioTrack() {
        return this.audioSource.createTrack();
    }
    createVideoTrack(width, height, framerate) {
        this.videoWidth = width;
        this.videoHeight = height;
        this.isVideo = true;
        this.videoFramerate = 1000 / framerate;
        return this.videoSource.createTrack();
    }
    setVideoParams(width, height, framerate) {
        this.videoWidth = width;
        this.videoHeight = height;
        this.videoFramerate = 1000 / framerate;
    }
    setAudioParams(bitrate) {
        this.sampleRate = bitrate;
    }
    bytesLength() {
        if (this.isVideo) {
            return 1.5 * this.videoWidth * this.videoHeight;
        }
        else {
            return ((this.sampleRate * this.bitsPerSample) / 8 / 100) * this.channelCount;
        }
    }
    processData() {
        const oldTime = new Date().getTime();
        if (this.stopped) {
            return;
        }
        const byteLength = this.bytesLength();
        this.lastDifferenceRemote = 0;
        if (!(!this.finished &&
            this.finishedLoading &&
            this.cache.length < byteLength) && this.filePath !== undefined) {
            try {
                if (this.needsBuffering(false)) {
                    let checkBuff = true;
                    if (this.timePulseBuffer > 0) {
                        this.runningPulse =
                            this.cache.length <
                                byteLength * this.needed_time() * this.timePulseBuffer;
                        checkBuff = this.runningPulse;
                    }
                    if (this.readable !== undefined && checkBuff) {
                        this.readable.resume();
                    }
                }
            }
            catch (e) {
                this.emit('stream_deleted');
                return;
            }
            const checkLag = this.checkLag();
            let fileSize;
            try {
                if (oldTime - this.lastByteCheck > 1000) {
                    fileSize = Stream.getFilesizeInBytes(this.filePath);
                    this.lastByte = fileSize;
                    this.lastByteCheck = oldTime;
                }
                else {
                    fileSize = this.lastByte;
                }
            }
            catch (e) {
                this.emit('stream_deleted');
                return;
            }
            const lagging_remote = this.isLaggingRemote();
            if (!this.paused &&
                !this.finished &&
                !lagging_remote &&
                (this.cache.length >= byteLength || this.finishedLoading) &&
                !checkLag) {
                this.playedBytes += byteLength;
                const buffer = this.cache.slice(0, byteLength);
                if (this.isVideo) {
                    const i420Frame = {
                        width: this.videoWidth,
                        height: this.videoHeight,
                        data: new Uint8ClampedArray(buffer)
                    };
                    this.videoSource.onFrame(i420Frame);
                }
                else {
                    const samples = new Int16Array(new Uint8Array(buffer).buffer);
                    this.audioSource.onData({
                        bitsPerSample: this.bitsPerSample,
                        sampleRate: this.sampleRate,
                        channelCount: this.channelCount,
                        numberOfFrames: samples.length,
                        samples,
                    });
                }
                this.cache = this.cache.slice(byteLength);
            }
            else if (checkLag) {
                binding_1.Binding.log('STREAM_LAG -> ' + new Date().getTime() +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
                binding_1.Binding.log('BYTES_STREAM_CACHE_LENGTH -> ' + this.cache.length +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
                binding_1.Binding.log('BYTES_LOADED -> ' +
                    this.bytesLoaded +
                    'OF -> ' +
                    Stream.getFilesizeInBytes(this.filePath) +
                    ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
            }
            if (!this.finishedLoading) {
                if (fileSize === this.lastBytesLoaded) {
                    if (this.equalCount >= 8) {
                        this.equalCount = 0;
                        binding_1.Binding.log('NOT_ENOUGH_BYTES -> ' + oldTime +
                            ' -> ' + (this.isVideo ? 'VIDEO' : 'AUDIO'), binding_1.Binding.DEBUG);
                        this.finishedBytes = true;
                        this.readable?.resume();
                    }
                    else {
                        if (oldTime - this.lastLag > 1000) {
                            this.equalCount += 1;
                            this.lastLag = oldTime;
                        }
                    }
                }
                else {
                    this.lastBytesLoaded = fileSize;
                    this.equalCount = 0;
                    this.finishedBytes = false;
                }
            }
        }
        if (!this.finished &&
            this.finishedLoading &&
            this.cache.length < byteLength &&
            this.filePath !== undefined) {
            this.finish();
            this.emit('finish');
        }
        const toSubtract = new Date().getTime() - oldTime;
        const timeoutWait = this.frameTime() - toSubtract - this.lastDifferenceRemote;
        setTimeout(() => this.processData(), timeoutWait > 0 ? timeoutWait : 1);
    }
    isLaggingRemote() {
        if (this.remotePlayingTime != undefined) {
            const remote_play_time = this.remotePlayingTime().time;
            const local_play_time = this.currentPlayedTime();
            if (remote_play_time != undefined && local_play_time != undefined) {
                if (local_play_time > remote_play_time) {
                    this.lastDifferenceRemote = (local_play_time - remote_play_time) * 10000;
                    return true;
                }
            }
        }
        return false;
    }
    frameTime() {
        return (this.finished || this.paused || this.checkLag() || this.filePath === undefined ? 500 : this.isVideo ? this.videoFramerate : 10);
    }
    currentPlayedTime() {
        if (this.filePath === undefined || this.playedBytes <= this.bytesLength() || this.finished) {
            return undefined;
        }
        else {
            return Math.floor((this.playedBytes / this.bytesLength()) / (0.0001 / this.frameTime()));
        }
    }
}
exports.Stream = Stream;
