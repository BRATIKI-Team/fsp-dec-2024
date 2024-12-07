export interface ResetPasswordRequest {
  readonly token: string;
  readonly password: string;
}

export interface ForgetPasswordRequest {
  readonly email: string;
}
