import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { login as apiLogin, verifyToken, getCurrentUser } from '../services/api';

interface User {
  email: string;
  full_name: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      // Verify token is still valid
      verifyToken(storedToken).then((response) => {
        if (response.data) {
          setUser(response.data);
          setToken(storedToken);
        } else {
          // Token invalid, clear it
          localStorage.removeItem('auth_token');
        }
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiLogin(email, password);

      if (response.error) {
        return { success: false, error: response.error };
      }

      if (response.data) {
        const { access_token } = response.data;

        // Store token
        localStorage.setItem('auth_token', access_token);
        setToken(access_token);

        // Get user info
        const userResponse = await getCurrentUser(access_token);
        if (userResponse.data) {
          setUser(userResponse.data);
        }

        return { success: true };
      }

      return { success: false, error: 'No data received' };
    } catch (error) {
      return { success: false, error: 'Login failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    setToken(null);
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user && !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
