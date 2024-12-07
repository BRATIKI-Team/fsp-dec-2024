export interface ICriterionStrings {
  readonly field: string;
  readonly value: string[];
}

export interface ICriterionDateRange {
  readonly field: string;
  readonly value: { readonly start: Date; readonly end: Date };
}

export type ICriterion = ICriterionStrings | ICriterionDateRange;

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
