"use client";

import { useState } from "react";
import { Analysis } from "../types";
import { EmotionBadge } from "./EmotionBadge";
import { RecommendationCard } from "./RecommendationCard";
import { SafetyAlert } from "./SafetyAlert";

interface AnalysisCardProps {
  analysis: Analysis;
}

export function AnalysisCard({ analysis }: AnalysisCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(analysis.suggested_response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case "low":
        return "bg-emerald-100 text-emerald-900 border-emerald-300";
      case "medium":
        return "bg-amber-100 text-amber-900 border-amber-300";
      case "high":
      case "critical":
        return "bg-red-100 text-red-900 border-red-300";
      default:
        return "bg-slate-100 text-slate-900 border-slate-300";
    }
  };

  return (
    <div className="space-y-6">
      {analysis.safety_warning && (
        <SafetyAlert warningMessage={analysis.safety_warning} />
      )}

      <div className="bg-white/95 backdrop-blur-md p-7 rounded-2xl border border-white/60 shadow-xl space-y-6">
        {/* Encabezado del Análisis */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider">
              Diagnóstico de IUnderstandYou
            </span>
            <h3 className="text-xl font-bold text-slate-900 mt-0.5">
              Análisis Interpersonal
            </h3>
          </div>
          <div className="flex items-center gap-2">
            <span className={`text-xs font-bold px-3 py-1 rounded-full border capitalize ${getRiskBadgeColor(analysis.risk_level)}`}>
              Riesgo: {analysis.risk_level}
            </span>
            <span className="text-xs font-medium text-slate-700 bg-slate-100 px-3 py-1 rounded-full border border-slate-200">
              Sensibilidad: {analysis.sensitivity_level}
            </span>
          </div>
        </div>

        {/* Resumen del Contexto */}
        <div>
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
            Resumen del Contexto
          </h4>
          <p className="text-sm text-slate-800 bg-emerald-50/50 p-4 rounded-xl border border-emerald-100 leading-relaxed">
            {analysis.context_summary}
          </p>
        </div>

        {/* Emoción Probable Detectada */}
        <div>
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
            Emoción Principal Detectada
          </h4>
          <div className="inline-block bg-teal-50 text-teal-900 font-semibold text-sm px-3.5 py-1.5 rounded-lg border border-teal-200/80">
            {analysis.detected_emotion}
          </div>
          <EmotionBadge emotions={analysis.emotions} />
        </div>

        {/* Recomendación Principal */}
        <div>
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">
            Recomendación Principal
          </h4>
          <p className="text-sm font-medium text-slate-900 bg-emerald-50 p-4.5 rounded-xl border border-emerald-200/70 leading-relaxed shadow-sm">
            🌿 {analysis.recommendation}
          </p>
        </div>

        {/* Respuesta Sugerida con Botón Copiar */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Respuesta Sugerida Adaptable
            </h4>
            <button
              onClick={handleCopy}
              className="text-xs font-medium text-emerald-800 hover:text-emerald-900 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200/80 transition-colors shadow-sm cursor-pointer"
            >
              {copied ? "✓ Copiado al portapapeles" : "📋 Copiar mensaje"}
            </button>
          </div>
          <blockquote className="text-sm italic text-slate-100 bg-slate-900 p-4.5 rounded-xl shadow-inner leading-relaxed border-l-4 border-emerald-500">
            {analysis.suggested_response}
          </blockquote>
        </div>

        {/* Componente de Alternativas */}
        <RecommendationCard recommendations={analysis.recommendations} />
      </div>
    </div>
  );
}
