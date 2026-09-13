"use client";

import { useEffect, useState } from "react";
import { getPreferencesApi, updatePreferencesApi } from "../../services/api";
import { UserPreferences } from "../../types";
import { useAuth } from "../../context/AuthContext";

export default function ProfilePage() {
  const { user } = useAuth();
  const [commStyle, setCommStyle] = useState<"empático" | "directo" | "analítico">("empático");
  const [directness, setDirectness] = useState<"directo" | "equilibrado" | "cuidadoso">("equilibrado");
  const [prefLength, setPrefLength] = useState<"corto" | "medio" | "largo">("medio");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    getPreferencesApi()
      .then((data) => {
        setCommStyle(data.communication_style);
        setDirectness(data.directness_level);
        setPrefLength(data.preferred_response_length);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      await updatePreferencesApi({
        communication_style: commStyle,
        directness_level: directness,
        preferred_response_length: prefLength,
      });
      setMessage("✓ Preferencias de comunicación guardadas correctamente.");
    } catch (err: any) {
      setMessage("❌ Error al guardar las preferencias.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-xl mx-auto px-4 py-8 text-center text-white text-sm bg-slate-900/30 backdrop-blur-sm rounded-xl">
        Cargando perfil...
      </div>
    );
  }

  return (
    <main className="max-w-xl mx-auto px-4 py-8 space-y-6">
      <div className="bg-white/95 backdrop-blur-md p-8 rounded-2xl border border-white/60 shadow-xl space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h2 className="text-2xl font-bold text-slate-900">Perfil y Preferencias</h2>
          <p className="text-sm text-slate-600 mt-1">
            Personaliza cómo IUnderstandYou formula sus sugerencias y alternativas de comunicación.
          </p>
        </div>

        {user && (
          <div className="bg-emerald-50/60 p-4 rounded-xl border border-emerald-200/80 flex items-center gap-3">
            <div className="w-10 h-10 bg-emerald-700 text-white font-bold text-lg rounded-full flex items-center justify-center">
              {user.name.charAt(0)}
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">{user.name}</h3>
              <p className="text-xs text-slate-600">{user.email}</p>
            </div>
          </div>
        )}

        {message && (
          <div className={`p-3.5 rounded-xl text-sm border ${message.startsWith("✓") ? "bg-emerald-50 border-emerald-200 text-emerald-900 font-medium" : "bg-red-50 border-red-200 text-red-900 font-medium"}`}>
            {message}
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-800 mb-1">
              Estilo de Comunicación Preferido
            </label>
            <select
              value={commStyle}
              onChange={(e) => setCommStyle(e.target.value as any)}
              className="w-full p-3.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm bg-white"
            >
              <option value="empático">Empático y Comprensivo</option>
              <option value="directo">Directo y Conciso</option>
              <option value="analítico">Analítico y Estructurado</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-800 mb-1">
              Nivel de Franqueza / Cuidado
            </label>
            <select
              value={directness}
              onChange={(e) => setDirectness(e.target.value as any)}
              className="w-full p-3.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm bg-white"
            >
              <option value="cuidadoso">Cuidadoso y Diplomático</option>
              <option value="equilibrado">Equilibrado</option>
              <option value="directo">Directo y Transparente</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-800 mb-1">
              Longitud de Respuesta Sugerida
            </label>
            <select
              value={prefLength}
              onChange={(e) => setPrefLength(e.target.value as any)}
              className="w-full p-3.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm bg-white"
            >
              <option value="corto">Corta (Frase directa)</option>
              <option value="medio">Media (1-2 oraciones claras)</option>
              <option value="largo">Detallada (Explicación amplia)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-xl transition-colors shadow-md disabled:opacity-50 text-sm cursor-pointer"
          >
            {saving ? "Guardando preferencias..." : "Guardar Preferencias"}
          </button>
        </form>
      </div>
    </main>
  );
}
