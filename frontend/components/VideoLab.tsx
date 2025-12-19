"use client";

import { useState } from "react";
import { Diagnosis } from "@/types";

export default function VideoLab() {
    const [url, setUrl] = useState("");
    const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState("");
    const [progress, setProgress] = useState(0);
    const [loadingStep, setLoadingStep] = useState("");
    const [error, setError] = useState("");

    const simulateProgress = () => {
        setProgress(5);
        setLoadingStep("Iniciando motor de descarga...");
        setTimeout(() => { setProgress(15); setLoadingStep("Descargando video de Instagram..."); }, 3000);
        setTimeout(() => { setProgress(30); setLoadingStep("Extrayendo frames clave para análisis..."); }, 10000);
        setTimeout(() => { setProgress(50); setLoadingStep("Enviando a Gemini Vision AI..."); }, 20000);
        setTimeout(() => { setProgress(70); setLoadingStep("Deconstruyendo patrones virales (Frame by Frame)..."); }, 35000);
        setTimeout(() => { setProgress(85); setLoadingStep("Redactando Guía de Producción y Blueprint..."); }, 50000);
        setTimeout(() => { setProgress(92); setLoadingStep("Finalizando ingeniería inversa..."); }, 65000);
    };

    const handleAnalyze = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url.trim()) return;

        // Validation: Ensure it's a specific video link
        const isVideoLink = url.includes("/reel/") || url.includes("/tiktok.com/") || url.includes("/shorts/");
        if (!isVideoLink) {
            setError("⚠️ Ese parece un link de perfil. Necesito el link de un VIDEO específico (Reel, TikTok o Short).");
            return;
        }

        setLoading(true);
        setProgress(0);
        setDiagnosis(null);
        setError("");
        simulateProgress();

        try {
            const res = await fetch("http://localhost:8000/api/analyze_video", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || "Error en el análisis. Verifica el link.");
            }

            const data = await res.json();
            setDiagnosis(data);
            setProgress(100);
        } catch (e: any) {
            setError(e.message || "Error desconocido");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8 animate-fade-in-up">
            <div className="bg-white rounded-xl p-8 card-shadow border border-slate-100 text-center">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">Laboratorio de ADN Viral 🧬</h2>
                <p className="text-slate-500 mb-6">Pega el link de un Reel o TikTok. La IA lo mirará cuadro por cuadro para decirte por qué funciona.</p>

                <form onSubmit={handleAnalyze} className="max-w-xl mx-auto flex gap-3">
                    <input
                        type="text"
                        placeholder="https://www.instagram.com/reel/..."
                        className="flex-1 bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-slate-800 focus:outline-none focus:border-purple-500 transition-colors"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg px-6 py-3 transition-colors disabled:opacity-50"
                    >
                        {loading ? "Decodificando..." : "Analizar Viralidad"}
                    </button>
                </form>

                {loading && (
                    <div className="mt-6 text-left max-w-xl mx-auto">
                        <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wide">
                            <span>{loadingStep}</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                            <div
                                className="bg-purple-500 h-full rounded-full transition-all duration-500 ease-out"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>
                        <p className="text-xs text-slate-400 mt-2 text-center animate-pulse">
                            Esto puede tomar hasta 60 segundos mientras la IA realiza la ingeniería inversa completa.
                        </p>
                    </div>
                )}

                {error && (
                    <div className="mt-4 text-red-500 bg-red-50 p-2 rounded">{error}</div>
                )}
            </div>

            {
                diagnosis && (
                    <div className="bg-[#1a1a1a] text-white rounded-xl p-8 shadow-2xl border border-purple-900/50 relative overflow-hidden">
                        <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-8">
                            <div className="md:col-span-2 space-y-6">
                                {/* MISSED OPPORTUNITIES / CRÍTICA DE ESCALADO */}
                                {diagnosis.missed_opportunities && diagnosis.missed_opportunities.length > 0 && (
                                    <div className="mt-8 bg-black/30 p-6 rounded-xl border border-red-500/20 relative">
                                        <h4 className="text-red-400 font-bold uppercase tracking-widest text-xs mb-4 flex items-center gap-2">
                                            <span>📉</span> ¿Por qué no llegó al Millón de Vistas?
                                        </h4>
                                        <ul className="space-y-3">
                                            {diagnosis.missed_opportunities.map((opp, idx) => (
                                                <li key={idx} className="flex gap-3 text-sm text-gray-300">
                                                    <span className="text-red-500/50 mt-1">⚠️</span>
                                                    <span>{opp}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* TAGS / CLASIFICACIÓN */}
                                {diagnosis.tags && (
                                    <div className="flex flex-wrap gap-2 mb-6">
                                        {diagnosis.tags.map((tag, idx) => (
                                            <span key={idx} className="bg-purple-900/50 text-purple-200 px-3 py-1 rounded-full text-xs font-bold border border-purple-500/30 uppercase tracking-wider">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                )}

                                <div>
                                    <h3 className="text-purple-400 font-bold uppercase tracking-widest text-sm mb-2">Ingeniería Inversa del Éxito</h3>
                                    <p className="text-xl font-light italic leading-relaxed mb-6">"{diagnosis.summary}"</p>
                                </div>

                                {/* VIRAL MECHANICS GRID */}
                                {diagnosis.viral_mechanics && (
                                    <div className="grid grid-cols-1 gap-4 mb-8">
                                        <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                                            <h4 className="text-emerald-400 font-bold text-xs uppercase mb-1">🪝 El Gancho (Hook)</h4>
                                            <p className="text-gray-300 text-sm">{diagnosis.viral_mechanics.hook}</p>
                                        </div>
                                        <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                                            <h4 className="text-blue-400 font-bold text-xs uppercase mb-1">🧠 Psicología de Retención</h4>
                                            <p className="text-gray-300 text-sm">{diagnosis.viral_mechanics.retention}</p>
                                        </div>
                                        <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                                            <h4 className="text-pink-400 font-bold text-xs uppercase mb-1">🎯 El Cierre (CTA)</h4>
                                            <p className="text-gray-300 text-sm">{diagnosis.viral_mechanics.cta}</p>
                                        </div>
                                    </div>
                                )}

                                {/* TIMELINE / ANALISIS SECUENCIA */}
                                {diagnosis.timeline && diagnosis.timeline.length > 0 && (
                                    <div className="space-y-4">
                                        <h4 className="text-slate-400 font-bold uppercase tracking-widest text-xs border-b border-white/10 pb-2">Línea de Tiempo Viral</h4>
                                        {diagnosis.timeline.map((item, idx) => (
                                            <div key={idx} className="flex gap-4 items-start group hover:bg-white/5 p-2 rounded transition-colors">
                                                <div className="shrink-0 bg-slate-800 text-slate-300 font-mono text-xs px-2 py-1 rounded">
                                                    {item.time}
                                                </div>
                                                <div>
                                                    <div className="font-bold text-white text-sm mb-1">{item.event}</div>
                                                    <div className="text-xs text-slate-400 leading-relaxed italic border-l-2 border-purple-500/30 pl-3">
                                                        "{item.why_it_works}"
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div className="flex flex-col h-full">
                                {/* PRODUCTION CARD (Themes: Connected to Gatillo) */}
                                <div className="bg-gradient-to-br from-[#2e1065] via-[#4c1d95] to-[#2e1065] p-8 rounded-3xl border border-purple-500/30 shadow-2xl relative overflow-hidden group hover:border-purple-500/50 transition-all duration-500 h-full">
                                    <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                                    <div className="absolute -top-20 -right-20 w-64 h-64 bg-fuchsia-500 rounded-full blur-[100px] opacity-20 group-hover:opacity-30 transition-opacity"></div>
                                    <div className="absolute -bottom-10 -right-10 text-[8rem] opacity-5 -rotate-12 pointer-events-none select-none grayscale group-hover:grayscale-0 transition-all duration-700">🎬</div>

                                    {diagnosis.difficulty_level && (
                                        <div className="flex items-center justify-between gap-6 mb-8 border-b border-purple-500/10 pb-6 relative z-10">
                                            <div>
                                                <div className="text-[10px] tracking-[0.3em] uppercase text-purple-200/60 font-bold mb-1">Dificultad de Réplica</div>
                                                <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-purple-50 to-purple-200 leading-none">
                                                    {diagnosis.difficulty_level.split(" ")[0]}
                                                </div>
                                            </div>
                                            <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center border border-purple-500/20 text-2xl shadow-[0_0_15px_rgba(168,85,247,0.1)]">
                                                📶
                                            </div>
                                        </div>
                                    )}

                                    {diagnosis.production_guide && (
                                        <div className="space-y-8 relative z-10">
                                            <div className="relative">
                                                <div className="absolute -left-4 top-0 bottom-0 w-1 bg-gradient-to-b from-purple-500/40 to-transparent rounded-full"></div>
                                                <p className="text-sm md:text-base text-purple-100/90 italic leading-relaxed pl-4 font-medium">
                                                    "{diagnosis.production_guide.explanation}"
                                                </p>
                                            </div>

                                            <div>
                                                <div className="flex items-center gap-2 mb-3">
                                                    <span className="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                                                    <div className="text-[10px] text-purple-400 uppercase font-black tracking-[0.2em]">Equipo Recomendado</div>
                                                </div>
                                                <div className="flex flex-wrap gap-2">
                                                    {diagnosis.production_guide.equipment?.map((item, idx) => (
                                                        <span key={idx} className="text-[11px] bg-purple-500/10 hover:bg-purple-500/20 text-purple-200 px-3 py-1.5 rounded-lg border border-purple-500/20 whitespace-normal text-left leading-tight transition-colors cursor-default font-medium break-words max-w-full">
                                                            {item}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>

                                            <div className="bg-gradient-to-r from-purple-500/10 to-transparent p-5 rounded-2xl border-l-4 border-purple-500">
                                                <div className="flex items-center gap-2 mb-2">
                                                    <div className="text-lg">💡</div>
                                                    <div className="text-xs text-purple-400 uppercase font-black tracking-[0.2em]">Tip Pro</div>
                                                </div>
                                                <p className="text-sm md:text-base text-white/90 font-medium leading-relaxed">
                                                    {diagnosis.production_guide.tips}
                                                </p>
                                            </div>

                                            {/* SETUP DE RODAJE (SHOOTING PLAN) */}
                                            <div className="mt-8 pt-8 border-t border-purple-500/10 relative">
                                                <div className="absolute top-8 left-0 text-4xl opacity-10">🎥</div>
                                                <div className="text-[10px] text-purple-400 uppercase font-bold tracking-[0.2em] mb-6 flex items-center gap-2">
                                                    <span className="w-8 h-[1px] bg-purple-500/50"></span>
                                                    Setup de Rodaje
                                                    <span className="w-full h-[1px] bg-purple-500/10"></span>
                                                </div>

                                                <div className="grid grid-cols-1 gap-6">
                                                    {/* Angles */}
                                                    <div className="space-y-3">
                                                        <div className="flex items-center gap-2 text-purple-200/50 text-xs font-mono uppercase tracking-wider">
                                                            <span className="text-purple-500">◈</span> Ángulos Clave
                                                        </div>
                                                        <div className="flex flex-wrap gap-2">
                                                            {(diagnosis.production_guide.shooting_plan?.angles || [
                                                                "Plano Medio (Waist Up) con profundidad de campo baja",
                                                                "Insert de manos para demostración de producto",
                                                                "Plano Holandés (Ligeramente inclinado) para dinamismo"
                                                            ]).map((angle, i) => (
                                                                <div key={i} className="bg-black/20 text-purple-100/90 px-3 py-2 rounded border border-white/5 text-xs font-medium flex items-center gap-2">
                                                                    <span className="w-1 h-1 bg-purple-500 rounded-full"></span>
                                                                    {angle}
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>

                                                    {/* Lighting */}
                                                    <div className="space-y-2">
                                                        <div className="flex items-center gap-2 text-purple-200/50 text-xs font-mono uppercase tracking-wider">
                                                            <span className="text-purple-500">☀</span> Iluminación
                                                        </div>
                                                        <p className="text-sm text-purple-100/80 leading-relaxed pl-4 border-l border-purple-500/20">
                                                            {diagnosis.production_guide.shooting_plan?.lighting || "Esquema Rembrandt: Luz principal suave a 45 grados (Softbox o Ventana), con un relleno negativo en el lado opuesto para contraste dramático."}
                                                        </p>
                                                    </div>

                                                    {/* Audio */}
                                                    <div className="space-y-2">
                                                        <div className="flex items-center gap-2 text-purple-200/50 text-xs font-mono uppercase tracking-wider">
                                                            <span className="text-purple-500">🎙</span> Audio
                                                        </div>
                                                        <p className="text-sm text-purple-100/80 leading-relaxed pl-4 border-l border-purple-500/20">
                                                            {diagnosis.production_guide.shooting_plan?.audio || "Micrófono de solapa oculto (o Shotgun direccional). Música Lo-Fi de fondo a -20db para no competir con la voz."}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>

                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* BLUEPRINT, TRIGGER & PRODUCTION GRID */}
                        {/* BLUEPRINT & TRIGGER GRID */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">

                            {/* BLUEPRINT / FÓRMULA */}
                            <div className="bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#0f172a] p-8 rounded-3xl border border-blue-500/20 shadow-2xl relative overflow-hidden group hover:border-blue-500/40 transition-all duration-500">
                                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
                                <div className="absolute -top-20 -right-20 w-64 h-64 bg-blue-500 rounded-full blur-[80px] opacity-10 group-hover:opacity-20 transition-opacity"></div>
                                <div className="absolute -bottom-6 -right-6 p-4 text-6xl opacity-10 pointer-events-none select-none grayscale group-hover:grayscale-0 transition-all duration-700">🧬</div>

                                <h4 className="relative z-10 text-blue-200/60 text-[10px] font-bold uppercase tracking-[0.3em] mb-8 flex items-center gap-3">
                                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full shadow-[0_0_10px_rgba(96,165,250,0.8)]"></span>
                                    Fórmula / Estructura
                                </h4>

                                <div className="flex flex-col gap-0 relative z-10 pl-2">
                                    {/* Vertical Line */}
                                    <div className="absolute left-[1.15rem] top-4 bottom-4 w-0.5 bg-gradient-to-b from-blue-500/30 to-transparent"></div>

                                    {diagnosis.structure_blueprint ? (
                                        diagnosis.structure_blueprint.split("+").map((step, idx) => (
                                            <div key={idx} className="relative flex items-center gap-5 mb-5 last:mb-0 group/step">
                                                <div className="w-10 h-10 rounded-full bg-[#0f172a] border border-blue-500/30 text-blue-400 flex items-center justify-center text-sm font-bold shrink-0 shadow-[0_0_15px_rgba(59,130,246,0.1)] group-hover/step:border-blue-400 group-hover/step:shadow-[0_0_20px_rgba(59,130,246,0.4)] group-hover/step:scale-110 transition-all duration-300 z-10">
                                                    {idx + 1}
                                                </div>
                                                <div className="bg-blue-500/5 hover:bg-blue-500/10 text-blue-100 px-5 py-3.5 rounded-xl border border-blue-500/10 text-sm font-medium shadow-sm backdrop-blur-sm w-full transition-all duration-300 hover:translate-x-1">
                                                    {step.replace(/[\[\]]/g, "").trim()}
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="text-slate-500 italic text-sm pl-4 flex items-center gap-2">
                                            <span className="animate-pulse">●</span> Decodificando estructura...
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* GATILLO EMOCIONAL */}
                            <div className="bg-gradient-to-br from-[#2e1065] via-[#4c1d95] to-[#2e1065] p-8 rounded-3xl border border-purple-500/30 shadow-2xl flex flex-col justify-center text-center relative overflow-hidden group hover:border-purple-500/50 transition-all duration-500">
                                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                                <div className="absolute -bottom-10 -left-10 text-[10rem] opacity-10 rotate-12 pointer-events-none select-none animate-pulse-slow">🎯</div>
                                <div className="absolute top-0 right-0 w-64 h-64 bg-fuchsia-500 rounded-full blur-[100px] opacity-20 group-hover:opacity-30 transition-opacity"></div>

                                <h4 className="relative z-10 text-purple-200/60 text-[10px] font-bold uppercase tracking-[0.3em] mb-6 border-b border-white/5 pb-4 mx-8">
                                    Gatillo Emocional
                                </h4>

                                <div className="relative z-10 flex flex-col items-center flex-grow justify-center">
                                    <div className="text-4xl md:text-5xl font-black text-white mb-4 drop-shadow-2xl tracking-tight leading-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-purple-50 to-purple-200">
                                        {diagnosis.psychological_trigger ? diagnosis.psychological_trigger.split("(")[0] : "Identificando..."}
                                    </div>
                                    {diagnosis.psychological_trigger && diagnosis.psychological_trigger.includes("(") && (
                                        <div className="text-purple-200/80 text-sm font-medium pt-2 max-w-[85%] leading-relaxed">
                                            {diagnosis.psychological_trigger.split("(")[1].replace(")", "")}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }
        </div >
    );
}
