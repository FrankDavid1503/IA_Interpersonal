import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "../context/AuthContext";
import { Navbar } from "../components/Navbar";
import { CalmMusicWidget } from "../components/CalmMusicWidget";

export const metadata: Metadata = {
  title: "IUnderstandYou — Agente de IA Personal",
  description: "Apoyo inteligente para decisiones interpersonales y bienestar personal",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="min-h-screen antialiased bg-slate-50 text-slate-900 flex flex-col relative">
        <AuthProvider>
          <Navbar />
          <div className="flex-1">
            {children}
          </div>
          <CalmMusicWidget />
        </AuthProvider>
      </body>
    </html>
  );
}
