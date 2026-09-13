"use client";

import { useEffect, useState } from "react";
import { getSituationsApi, deleteSituationApi } from "../../services/api";
import { Situation } from "../../types";
import Link from "next/link";
import { useAuth } from "../../context/AuthContext";

export default function HistoryPage() {
  const { user, loading: authLoading } = useAuth();
  const [situations, setSituations] = useState<Situation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = () => {
    setLoading(true);
    getSituationsApi()
      .then((data) => setSituations(data))
      .catch((err) => setError(err.message || "Error al cargar historial."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (user) {
      fetchHistory();
    }
  }, [user]);

  const handleDelete = async (id: string) => {
    if (confirm("¿Estás seguro de que deseas eliminar este análisis de tu historial?")) {
      try {
        await deleteSituationApi(id);
        setSituations((prev) => prev.filter((s) => s.id !== id));
      } catch (err: any) {
        alert(err.message || "Error al eliminar la situación.");
      }
    }
  };

  if (authLoading || loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center text-white text-sm bg-slate-900/30 backdrop-blur-sm rounded-xl">
        Cargando historial...
      </div>
    );
  }

  return (
    <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="bg-white/95 backdrop-blur-md p-6 rounded-2xl border border-white/60 shadow-xl flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Historial de Análisis</h2>
          <p className="text-sm text-slate-600 mt-1">
            Consulta tus situaciones previas y los diagnósticos generados por IUnderstandYou.
          </p>
        </div>
        <Link
          href="/dashboard"
          className="px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold text-sm rounded-xl transition-colors shadow-md"
        >
          + Nueva Situación
        </Link>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl">
          {error}
        </div>
      )}

      {situations.length === 0 ? (
        <div className="bg-white/95 backdrop-blur-md p-12 text-center rounded-2xl border border-white/60 shadow-xl space-y-3">
          <span className="text-4xl">📝</span>
          <h3 className="text-lg font-bold text-slate-800">Aún no tienes situaciones guardadas</h3>
          <p className="text-sm text-slate-500 max-w-md mx-auto">
            Ingresa tu primera situación interpersonal en el dashboard para recibir un diagnóstico completo con alternativas.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {situations.map((sit) => (
            <div
              key={sit.id}
              className="bg-white/95 backdrop-blur-md p-6 rounded-2xl border border-white/60 shadow-lg hover:shadow-xl transition-shadow flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-0.5 rounded-full capitalize">
                    {sit.relationship_type}
                  </span>
                  <span className="text-xs text-slate-500">
                    {new Date(sit.created_at).toLocaleDateString("es-ES", {
                      day: "numeric",
                      month: "short",
                      year: "numeric",
                    })}
                  </span>
                </div>
                <p className="text-sm font-medium text-slate-900 line-clamp-2 leading-relaxed">
                  "{sit.input_text}"
                </p>
                <p className="text-xs text-slate-500">
                  <strong className="text-slate-700">Objetivo:</strong> {sit.objective}
                </p>
              </div>

              <div className="flex items-center gap-3 self-end md:self-center">
                <Link
                  href={`/analysis/${sit.id}`}
                  className="px-4 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 text-xs font-semibold rounded-xl transition-colors border border-emerald-200"
                >
                  Ver análisis
                </Link>
                <button
                  onClick={() => handleDelete(sit.id)}
                  className="p-2 text-slate-400 hover:text-red-600 transition-colors text-xs font-semibold cursor-pointer"
                  title="Eliminar registro"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
