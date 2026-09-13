import { User, Situation, Analysis, AuthToken, UserPreferences } from "../types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("nexo_token") : null;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = "Ocurrió un error en la solicitud.";
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === "string" 
          ? errorData.detail 
          : JSON.stringify(errorData.detail);
      }
    } catch (_) {}
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}

// Autenticación API
export async function registerApi(name: string, email: string, password: string): Promise<User> {
  return apiFetch<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  });
}

export async function loginApi(email: string, password: string): Promise<AuthToken> {
  return apiFetch<AuthToken>("/auth/login/json", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getMeApi(): Promise<User> {
  return apiFetch<User>("/auth/me");
}

// Situaciones API
export async function createSituationApi(input_text: string, relationship_type: string, objective: string): Promise<Situation> {
  return apiFetch<Situation>("/situations", {
    method: "POST",
    body: JSON.stringify({ input_text, relationship_type, objective }),
  });
}

export async function getSituationsApi(): Promise<Situation[]> {
  return apiFetch<Situation[]>("/situations");
}

export async function getSituationApi(id: string): Promise<Situation> {
  return apiFetch<Situation>(`/situations/${id}`);
}

export async function deleteSituationApi(id: string): Promise<{ message: string }> {
  return apiFetch<{ message: string }>(`/situations/${id}`, {
    method: "DELETE",
  });
}

// Análisis de IA API
export async function analyzeSituationApi(situation_id: string): Promise<Analysis> {
  return apiFetch<Analysis>(`/situations/${situation_id}/analyze`, {
    method: "POST",
  });
}

export async function getAnalysisApi(analysis_id: string): Promise<Analysis> {
  return apiFetch<Analysis>(`/analyses/${analysis_id}`);
}

// Preferencias API
export async function getPreferencesApi(): Promise<UserPreferences> {
  return apiFetch<UserPreferences>("/preferences");
}

export async function updatePreferencesApi(pref: Partial<UserPreferences>): Promise<UserPreferences> {
  return apiFetch<UserPreferences>("/preferences", {
    method: "PUT",
    body: JSON.stringify(pref),
  });
}
