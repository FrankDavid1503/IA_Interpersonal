export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface UserPreferences {
  id: string;
  user_id: string;
  communication_style: "empático" | "directo" | "analítico";
  directness_level: "directo" | "equilibrado" | "cuidadoso";
  preferred_response_length: "corto" | "medio" | "largo";
}

export interface Situation {
  id: string;
  user_id: string;
  input_text: string;
  relationship_type: string;
  objective: string;
  created_at: string;
}

export interface Emotion {
  id: string;
  emotion: string;
  confidence: number;
  created_at: string;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  benefit?: string;
  risk?: string;
  priority: number;
  created_at: string;
}

export interface Analysis {
  id: string;
  situation_id: string;
  context_summary: string;
  detected_emotion: string;
  sensitivity_level: "low" | "medium" | "high";
  risk_level: "low" | "medium" | "high" | "critical";
  recommendation: string;
  suggested_response: string;
  model_name: string;
  created_at: string;
  emotions: Emotion[];
  recommendations: Recommendation[];
  safety_warning?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}
