import { create } from 'zustand';
import { UserProfile, AuthTokens } from '../../../../shared/types';

interface AuthState {
  user: UserProfile | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  setAuth: (user: UserProfile, tokens: AuthTokens) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  tokens: localStorage.getItem('access_token')
    ? { access_token: localStorage.getItem('access_token')!, refresh_token: '', token_type: 'bearer', expires_in: 3600 }
    : null,
  isAuthenticated: !!localStorage.getItem('access_token'),

  setAuth: (user, tokens) => {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', tokens.access_token);
    set({ user, tokens, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    set({ user: null, tokens: null, isAuthenticated: false });
  }
}));
