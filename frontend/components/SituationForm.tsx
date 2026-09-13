"use client";

import { useState } from "react";
import { createSituationApi, analyzeSituationApi } from "../services/api";
import { Analysis } from "../types";

interface SituationFormProps {
  onAnalysisComplete: (analysis: Analysis) => void;
}

export function SituationForm({ onAnalysisComplete }: SituationFormProps) {
  const [mode, setMode] = useState<"interpersonal" | "personal">("interpersonal");
  const [inputText, setInputText] = useState("");
  
  // Estado para modo Interpersonal (Analizar situación de otra persona)
  const [interpersonalRelationship, setInterpersonalRelationship] = useState("amigo");
  const [interpersonalObjective, setInterpersonalObjective] = useState("saber qué hacer, cómo actuar");

  // Estado para modo Personal (Cuando me siento mal)
  const [personalObjective, setPersonalObjective] = useState("Encontrar calma, claridad y palabras de consuelo");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setError(null);
    setLoading(true);

    try {
      const relType = mode === "personal" ? "conmigo_mismo (autocuidado)" : interpersonalRelationship;
      const objText = mode === "personal" 
        ? (personalObjective || "Encontrar apoyo emocional y autocuidado") 
        : (interpersonalObjective || "Saber cómo actuar o qué responder");

      // 1. Crear registro de situación en base de datos
      const situation = await createSituationApi(inputText, relType, objText);
      
      // 2. Invocar análisis del agente de IA
      const analysis = await analyzeSituationApi(situation.id);
      
      // 3. Notificar finalización de análisis
      onAnalysisComplete(analysis);
    } catch (err: any) {
      setError(err.message || "Error al procesar la situación.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white/95 backdrop-blur-md p-7 rounded-2xl border border-white/60 shadow-xl space-y-6">
      {/* Selector de Modo: Interpersonal (Otra persona) vs Personal (Autocuidado) */}
      <div className="flex bg-slate-100 p-1.5 rounded-xl border border-slate-200/80 gap-2">
        <button
          type="button"
          onClick={() => setMode("interpersonal")}
          className={`flex-1 py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
            mode === "interpersonal"
              ? "bg-emerald-700 text-white shadow-md"
              : "text-slate-700 hover:text-slate-900 hover:bg-slate-200/60"
          }`}
        >
          <span>👥</span>
          <span>Analizar situación de otra persona</span>
        </button>
        <button
          type="button"
          onClick={() => setMode("personal")}
          className={`flex-1 py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
            mode === "personal"
              ? "bg-teal-700 text-white shadow-md"
              : "text-slate-700 hover:text-slate-900 hover:bg-slate-200/60"
          }`}
        >
          <span>💙</span>
          <span>Apoyo Personal / Me siento mal</span>
        </button>
      </div>

      <div className="mb-2">
        <h3 className="text-xl font-bold text-slate-900">
          {mode === "interpersonal"
            ? "¿Qué situación quieres analizar?"
            : "Espacio de Apoyo Personal & Autocuidado"}
        </h3>
        <p className="text-sm text-slate-600 mt-1 leading-relaxed">
          {mode === "interpersonal"
            ? "Describe lo que está sucediendo de forma clara. IUnderstandYou evaluará el contexto, la emoción y te sugerirá alternativas de respuesta."
            : "Escribe cómo te sientes, qué te abruma o qué estás experimentando. IUnderstandYou te ofrecerá palabras de consuelo, claridad y consejos de paz."}
        </p>
      </div>

      {error && (
        <div className="p-3.5 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-semibold text-slate-800 mb-1">
            {mode === "interpersonal"
              ? "Descripción de la situación"
              : "¿Cómo te sientes o qué estás atravesando?"}
          </label>
          <textarea
            required
            rows={4}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={
              mode === "interpersonal"
                ? "Ejemplo: Murió un familiar de un amigo y no sé cómo responderle o cómo actuar para apoyarlo..."
                : "Ejemplo: Me siento muy triste y abrumado hoy sin saber exactamente por qué. Necesito un consejo de paz mental..."
            }
            className="w-full p-4 border border-slate-300/80 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm leading-relaxed bg-white shadow-inner"
          />
        </div>

        {mode === "interpersonal" ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-800 mb-1">
                Vínculo o relación
              </label>
              <select
                value={interpersonalRelationship}
                onChange={(e) => setInterpersonalRelationship(e.target.value)}
                className="w-full px-4 py-3 border border-slate-300/80 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm bg-white"
              >
                <option value="amigo">Amigo / Amiga</option>
                <option value="familiar">Familiar</option>
                <option value="compañero">Compañero de trabajo / estudio</option>
                <option value="pareja">Pareja</option>
                <option value="otro">Otro</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-800 mb-1">
                ¿Qué buscas lograr?
              </label>
              <input
                type="text"
                required
                value={interpersonalObjective}
                onChange={(e) => setInterpersonalObjective(e.target.value)}
                placeholder="Ej: Saber qué hacer, cómo actuar"
                className="w-full px-4 py-3 border border-slate-300/80 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none text-slate-900 text-sm bg-white"
              />
            </div>
          </div>
        ) : (
          <div>
            <label className="block text-sm font-semibold text-slate-800 mb-1">
              ¿Qué necesitas en este momento?
            </label>
            <input
              type="text"
              required
              value={personalObjective}
              onChange={(e) => setPersonalObjective(e.target.value)}
              placeholder="Ej: Encontrar calma, claridad y palabras de consuelo"
              className="w-full px-4 py-3 border border-slate-300/80 rounded-xl focus:ring-2 focus:ring-teal-600 focus:border-teal-600 outline-none text-slate-900 text-sm bg-white"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !inputText.trim()}
          className={`w-full py-3.5 text-white font-semibold rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-50 text-sm flex items-center justify-center gap-2 mt-3 cursor-pointer ${
            mode === "personal" ? "bg-teal-700 hover:bg-teal-800" : "bg-emerald-700 hover:bg-emerald-800"
          }`}
        >
          {loading ? (
            <>
              <span className="animate-spin text-lg">🌿</span>
              <span>IUnderstandYou está analizando la situación...</span>
            </>
          ) : (
            <>
              <span>{mode === "personal" ? "💙 Recibir Apoyo y Consejos" : "✨ Analizar situación con IA"}</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
