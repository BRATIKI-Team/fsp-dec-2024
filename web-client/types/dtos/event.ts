import type { FileResponse } from '~/types/dtos/file';
import type { IRegion } from '~/types/dtos/region';
import type { IRequest } from '~/types/dtos/request';
import type { IUser } from '~/types/dtos/user';

export interface IEvent {
  readonly id: string;
  readonly name: string;
  readonly subject: string;
  readonly region_id?: string;
  readonly discipline: string;
  readonly start_date: Date;
  readonly end_date: Date;
  readonly location: string;
  readonly participants_count: number;
  readonly description?: string;
  readonly documents_ids: string[];
  readonly protocols_ids: string[];
  readonly is_approved_event?: string;
  readonly member_created_id?: string;
}

export interface IEventDetail {
  readonly event: IEvent;
  readonly region?: IRegion;
  readonly user?: IUser;
  readonly protocols: readonly FileResponse[];
  readonly documents: readonly FileResponse[];
  readonly results: readonly FileResponse[];
  readonly request: IRequest | null;
}

export interface IEventCreateRequest {
  name: string;
  discipline: string;
  description: string;
  start_date: string;
  end_date: string;
  participants_count: number;
  location: string;
  documents_ids: string[];
  protocols_ids: string[];
}
