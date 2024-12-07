import type { IUser } from '~/types/dtos/user';

export interface IMemberRequest {
  readonly id: string;
  readonly region_id: string;
  readonly user_id: string;
  readonly user: IUser;
  readonly status: string;
}