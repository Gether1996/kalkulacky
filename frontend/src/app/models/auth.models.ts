export interface User {
  email: string;
  first_name?: string;
  last_name?: string;
  is_active?: boolean;
  oauth_provider?: string | null;
  date_joined?: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

export interface LoginResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface RegisterResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface GoogleAuthRequest {
  token: string;
}

export interface GoogleAuthResponse {
  user: User;
  access: string;
  refresh: string;
  created: boolean;
}

export interface CheckAuthResponse {
  authenticated: boolean;
  user: User | null;
}
