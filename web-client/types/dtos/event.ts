import type { IRegion } from '~/types/dtos/region';
import type { IUser } from '~/types/dtos/user';

export interface IEvent {
  readonly id: number;
  readonly name: string;
  readonly region_id?: string;
  readonly discipline: string;
  readonly datetime: Date;
  readonly description?: string;
  readonly is_approved_event?: string;
  readonly member_created_id?: string;
}

export interface IEventDetail {
  readonly event: IEvent;
  readonly region?: IRegion;
  readonly user?: IUser;
}
