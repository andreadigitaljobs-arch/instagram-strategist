"use client";
import AnalysisDashboard from "@/components/AnalysisDashboard";
import VideoLab from "@/components/VideoLab";
import { useState } from "react";

export default function Home() {
  const [currentTab, setCurrentTab] = useState<"audit" | "video">("audit");

  return (
    <div className="flex min-h-screen bg-[#f1f5f9]">
      {/* Sidebar (Metricool Style) */}
      <aside className="w-64 bg-white border-r border-slate-200 hidden md:flex flex-col fixed h-full z-10">
        <div className="p-6 border-b border-slate-100">
          <h1 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span className="w-8 h-8 bg-blue-600 text-white rounded-lg flex items-center justify-center text-sm">S</span>
            Strategist
          </h1>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          <div className="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">Analítica</div>

          <button
            onClick={() => setCurrentTab("audit")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-colors ${currentTab === "audit" ? "text-blue-600 bg-blue-50" : "text-slate-600 hover:bg-slate-50"
              }`}
          >
            <span>📊</span> Auditoría
          </button>

          <button
            onClick={() => setCurrentTab("video")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${currentTab === "video" ? "text-purple-600 bg-purple-50 font-medium" : "text-slate-600 hover:bg-slate-50"
              }`}
          >
            <span>🎥</span> Video Lab <span className="text-[10px] bg-purple-100 text-purple-600 px-1.5 py-0.5 rounded-full ml-auto">Pro</span>
          </button>
        </nav>

        <div className="p-4 border-t border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-slate-200"></div>
            <div className="text-sm">
              <div className="font-medium text-slate-700">Usuario</div>
              <div className="text-xs text-slate-400">Plan Free</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 md:ml-64">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-20">
          <h2 className="font-semibold text-slate-700">
            {currentTab === "audit" ? "Auditoría de Perfil" : "Laboratorio de Video IA"}
          </h2>
          <button className="text-sm text-slate-500 hover:text-blue-600 transition-colors">Ayuda</button>
        </header>

        <div className="p-8 max-w-7xl mx-auto">
          {currentTab === "audit" ? <AnalysisDashboard /> : <VideoLab />}
        </div>
      </main>
    </div>
  );
}
