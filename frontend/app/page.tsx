import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-[85vh] flex flex-col items-center justify-center p-4 text-center">
      <div className="max-w-2xl bg-white/95 backdrop-blur-md p-10 rounded-2xl shadow-2xl border border-white/60 space-y-6">
        <div className="flex flex-col items-center gap-3">
          <img src="/logo.jpg" alt="IUnderstandYou Logo" className="w-24 h-24 object-contain rounded-2xl shadow-md border border-emerald-100 bg-white p-1" />
          <div className="inline-block bg-emerald-100 text-emerald-900 text-xs font-bold px-3.5 py-1 rounded-full border border-emerald-300 uppercase tracking-wider">
            Inteligencia Emocional & Autocuidado
          </div>
        </div>

        <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          IUnderstandYou — Agente de IA Personal
        </h1>
        
        <p className="text-base text-slate-700 leading-relaxed max-w-xl mx-auto">
          Plataforma de apoyo inteligente para comprender situaciones interpersonales, evaluar emociones, tomar decisiones empáticas y encontrar tranquilidad.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            href="/dashboard"
            className="px-6 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold text-sm rounded-xl transition-all shadow-md hover:shadow-lg"
          >
            Ir al Dashboard
          </Link>
          <Link
            href="/login"
            className="px-6 py-3 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 font-semibold text-sm rounded-xl transition-colors border border-emerald-200 shadow-sm"
          >
            Iniciar Sesión
          </Link>
        </div>
      </div>
    </main>
  );
}
