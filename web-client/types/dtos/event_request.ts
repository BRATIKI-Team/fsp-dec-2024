import type { IRegion } from '~/types/dtos/region';
import type { IEvent } from '~/types/dtos/event';

export interface IEventRequest {
  readonly id: string;
  readonly status: string;
  readonly canceled_reason: string|null;
  readonly region: IRegion;
  readonly event: IEvent;
}