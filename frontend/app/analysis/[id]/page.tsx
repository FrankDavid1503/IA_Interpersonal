"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getAnalysisApi } from "../../../services/api";
import { Analysis } from "../../../types";
import { AnalysisCard } from "../../../components/AnalysisCard";
import Link from "next/link";

export default function AnalysisDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAnalysis = () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    getAnalysisApi(id)
      .then((data) => setAnalysis(data))
      .catch((err) => setError(err.message || "Error al cargar el análisis."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAnalysis();
  }, [id]);

  return (
    <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between">
        <Link
          href="/history"
          className="text-xs font-semibold text-emerald-900 bg-white/95 backdrop-blur-md px-4 py-2.5 rounded-xl border border-white/60 shadow-md hover:bg-emerald-50 transition-colors flex items-center gap-1.5"
        >
          <span>←</span>
          <span>Volver al historial</span>
        </Link>
      </div>

      {loading && (
        <div className="bg-white/95 backdrop-blur-md p-12 text-center rounded-2xl border border-white/60 shadow-xl space-y-3">
          <span className="animate-spin text-3xl inline-block">🌿</span>
          <p className="text-sm font-semibold text-slate-700">
            NEXO está recuperando el resultado del análisis...
          </p>
        </div>
      )}

      {error && (
        <div className="bg-white/95 backdrop-blur-md p-6 rounded-2xl border border-red-200/80 shadow-xl space-y-3">
          <div className="p-4 bg-red-50 text-red-700 text-sm rounded-xl border border-red-200">
            {error}
          </div>
          <button
            onClick={loadAnalysis}
            className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold rounded-xl transition-colors shadow-sm cursor-pointer"
          >
            Reintentar cargar análisis
          </button>
        </div>
      )}

      {analysis && <AnalysisCard analysis={analysis} />}
    </main>
  );
}
