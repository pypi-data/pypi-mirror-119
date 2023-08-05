"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Binding = void 0;
const events_1 = require("events");
class Binding extends events_1.EventEmitter {
    constructor() {
        super();
        this.connected = false;
        this.promises = new Map();
        process.stdin.on('data', (chunk) => {
            try {
                const list_data = chunk.toString().replace('}{', '}\n{').split('\n');
                for (let i = 0; i < list_data.length; i++) {
                    const data = JSON.parse(list_data[i]);
                    if (data.try_connect == 'connected') {
                        this.connected = true;
                        Binding.sendInternalUpdate({
                            ping: true,
                        });
                        setInterval(() => Binding.sendInternalUpdate({
                            ping: true,
                        }), 10000);
                        this.emit('connect', data.user_id);
                    }
                    else if (data.ping_with_response) {
                        Binding.sendInternalUpdate({
                            ping_with_response: true,
                        });
                    }
                    else if (data.ssid == this.ssid) {
                        if (data.uid !== undefined) {
                            const promise = this.promises.get(data.uid);
                            if (promise) {
                                if (data.data !== undefined) {
                                    promise(data.data);
                                }
                                else {
                                    promise(null);
                                }
                            }
                        }
                        else {
                            this.emit('request', data.data);
                        }
                    }
                }
            }
            catch (e) {
                Binding.log('Invalid Binding Update', Binding.ERROR);
            }
        });
        this.ssid = Binding.makeID(12);
        Binding.sendInternalUpdate({
            try_connect: this.ssid,
        });
    }
    async sendUpdate(update) {
        if (this.connected) {
            const uid = Binding.makeID(12);
            Binding.sendInternalUpdate({
                uid,
                data: update,
                ssid: this.ssid,
            });
            return new Promise(resolve => {
                this.promises.set(uid, (data) => {
                    resolve(data);
                    this.promises.delete(uid);
                });
            });
        }
        else {
            throw new Error('No connected client');
        }
    }
    static log(message, verbose_mode) {
        Binding.sendInternalUpdate({
            log_message: message,
            verbose_mode: verbose_mode,
        });
    }
    static makeID(length) {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result;
    }
    static sendInternalUpdate(update) {
        console.log(JSON.stringify(update));
    }
}
exports.Binding = Binding;
Binding.DEBUG = 1;
Binding.INFO = 2;
Binding.WARNING = 3;
Binding.ERROR = 4;
