export interface IRegion {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly subject: string;
  readonly person: string;
  readonly is_main: boolean;
  readonly contacts: IContacts;
}

export interface IContacts {
  readonly email: string;
  readonly phone?: string;
  readonly social_links?: readonly string[];
}
