"use client";

import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { SituationForm } from "../../components/SituationForm";
import { AnalysisCard } from "../../components/AnalysisCard";
import { Analysis } from "../../types";

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const [activeAnalysis, setActiveAnalysis] = useState<Analysis | null>(null);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center text-white text-sm bg-slate-900/40 backdrop-blur-sm">
        Cargando perfil...
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center p-4 text-center">
        <div className="bg-white/95 backdrop-blur-md p-8 rounded-2xl border border-white/60 shadow-xl max-w-md">
          <h2 className="text-xl font-bold text-slate-900 mb-2">Acceso restringido</h2>
          <p className="text-sm text-slate-600 mb-6">Debes iniciar sesión para consultar el dashboard.</p>
          <a href="/login" className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-sm font-medium transition-colors shadow-sm inline-block">
            Ir al Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <main className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Banner con tonos de serenidad y tranquilidad */}
      <div className="bg-gradient-to-r from-emerald-800 via-teal-800 to-slate-900 p-7 rounded-2xl text-white shadow-lg border border-white/20">
        <h2 className="text-2xl font-bold tracking-tight">¡Hola, {user.name}! 👋</h2>
        <p className="text-emerald-100 text-sm mt-1 leading-relaxed">
          Analiza cualquier situación interpersonal y toma decisiones reflexivas antes de responder.
        </p>
      </div>

      <SituationForm onAnalysisComplete={(analysis) => setActiveAnalysis(analysis)} />

      {activeAnalysis && (
        <div className="pt-2">
          <AnalysisCard analysis={activeAnalysis} />
        </div>
      )}
    </main>
  );
}
