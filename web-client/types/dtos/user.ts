import type { IRegion } from '~/types/dtos/region';

export interface IUser {
  readonly id: string;
  readonly email: string;
  readonly role: UserRole;
  readonly region: IRegion | null;
  readonly contacts: {
    readonly email: string
    readonly phone: string
    readonly social_links: string[]
  }
}

export enum UserRole {
  SUPER_ADMIN = 'super-admin',
  ADMIN = 'admin',
  MEMBER = 'member',
  USER = 'user',
}
