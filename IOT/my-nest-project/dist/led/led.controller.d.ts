import { LedService } from './led.service';
export declare class LedController {
    private readonly ledService;
    constructor(ledService: LedService);
    turnOnLed(): Promise<{
        state: string;
    }>;
    turnOffLed(): Promise<{
        state: string;
    }>;
}
