import type { IRegion } from '~/types/dtos/region';

export interface IEvent {
  readonly id: number;
  readonly name: string;
  readonly region?: IRegion;
  readonly discipline: string;
  readonly datetime: Date;
  readonly description?: string;
  readonly is_approved_event?: string;
  readonly member_created_id?: string;
}
