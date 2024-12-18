"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.LedService = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("axios");
let LedService = class LedService {
    constructor() {
        this.espIp = '128.10.0.92';
    }
    async setLedState(state) {
        try {
            const response = await axios_1.default.get(`http://${this.espIp}/setLedState?state=${state}`);
            return response.data;
        }
        catch (error) {
            throw new Error(`Failed to set LED state: ${error.message}`);
        }
    }
};
exports.LedService = LedService;
exports.LedService = LedService = __decorate([
    (0, common_1.Injectable)()
], LedService);
//# sourceMappingURL=led.service.js.map