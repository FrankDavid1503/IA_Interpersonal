"use client";

import Link from "next/link";
import { useAuth } from "../context/AuthContext";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white/90 backdrop-blur-md border-b border-white/40 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <img src="/logo.jpg" alt="IUnderstandYou Logo" width={36} height={36} style={{ width: "36px", height: "36px", objectFit: "contain" }} className="w-9 h-9 object-contain rounded-lg shadow-sm" />
          <span className="bg-emerald-700 text-white font-black text-lg px-3 py-1 rounded-lg tracking-wider shadow-sm">
            IUnderstandYou
          </span>
          <span className="font-semibold text-slate-800 text-sm hidden sm:inline-block">
            Asistente Interpersonal & Personal
          </span>
        </Link>

        <nav className="flex items-center gap-6">
          {user ? (
            <>
              <Link href="/dashboard" className="text-sm font-medium text-slate-800 hover:text-emerald-700 transition-colors">
                Dashboard
              </Link>
              <Link href="/history" className="text-sm font-medium text-slate-800 hover:text-emerald-700 transition-colors">
                Historial
              </Link>
              <Link href="/profile" className="text-sm font-medium text-slate-800 hover:text-emerald-700 transition-colors">
                Perfil
              </Link>
              <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
                <span className="text-xs font-semibold text-slate-700 bg-emerald-50 text-emerald-900 border border-emerald-200 px-3 py-1 rounded-full">
                  {user.name}
                </span>
                <button
                  onClick={logout}
                  className="text-xs font-medium text-red-600 hover:text-red-800 transition-colors"
                >
                  Cerrar sesión
                </button>
              </div>
            </>
          ) : (
            <>
              <Link href="/login" className="text-sm font-medium text-slate-800 hover:text-emerald-700 transition-colors">
                Iniciar sesión
              </Link>
              <Link
                href="/register"
                className="text-sm font-medium bg-emerald-700 text-white px-4 py-2 rounded-lg hover:bg-emerald-800 transition-colors shadow-sm"
              >
                Registrarse
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
