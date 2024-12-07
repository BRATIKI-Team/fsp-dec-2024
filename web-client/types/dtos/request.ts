export interface IRequest {
  readonly id: string;
  readonly event_id: string;
  readonly region_id: string;
  readonly status: EventRequestStatus;
  readonly canceled_reason?: string;
}

export enum EventRequestStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  DECLINED = 'declined',
}
