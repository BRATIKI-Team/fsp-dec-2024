export interface ICriterion {
  readonly field: string;
  readonly value: string[];
}

export interface ISearchRequest {
  readonly page: number;
  readonly page_size: number;
  readonly criteria: readonly ICriterion[];
}

export interface ISearchResponse<T> {
  readonly total: number;
  readonly page: number;
  readonly page_size: number;
  readonly items: readonly T[];
  readonly more: boolean;
}
