"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.LedController = void 0;
const common_1 = require("@nestjs/common");
const led_service_1 = require("./led.service");
let LedController = class LedController {
    constructor(ledService) {
        this.ledService = ledService;
    }
    async turnOnLed() {
        const state = await this.ledService.setLedState('on');
        return { state };
    }
    async turnOffLed() {
        const state = await this.ledService.setLedState('off');
        return { state };
    }
};
exports.LedController = LedController;
__decorate([
    (0, common_1.Get)('on'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], LedController.prototype, "turnOnLed", null);
__decorate([
    (0, common_1.Get)('off'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], LedController.prototype, "turnOffLed", null);
exports.LedController = LedController = __decorate([
    (0, common_1.Controller)('led'),
    __metadata("design:paramtypes", [led_service_1.LedService])
], LedController);
//# sourceMappingURL=led.controller.js.map