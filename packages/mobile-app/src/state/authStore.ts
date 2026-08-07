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
  user: null,
  tokens: null,
  isAuthenticated: false,

  setAuth: (user, tokens) => set({ user, tokens, isAuthenticated: true }),
  logout: () => set({ user: null, tokens: null, isAuthenticated: false })
}));
