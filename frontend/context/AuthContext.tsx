"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User } from "../types";
import { getMeApi, loginApi, registerApi } from "../services/api";
import { useRouter } from "next/navigation";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const savedToken = localStorage.getItem("nexo_token");
    if (savedToken) {
      setToken(savedToken);
      getMeApi()
        .then((userData) => setUser(userData))
        .catch(() => logout())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const data = await loginApi(email, password);
    localStorage.setItem("nexo_token", data.access_token);
    setToken(data.access_token);
    const userData = await getMeApi();
    setUser(userData);
    router.push("/dashboard");
  };

  const register = async (name: string, email: string, password: string) => {
    await registerApi(name, email, password);
    await login(email, password);
  };

  const logout = () => {
    localStorage.removeItem("nexo_token");
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth debe ser usado dentro de un AuthProvider");
  }
  return context;
}
