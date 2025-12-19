"use client";

import { Profile, Diagnosis } from "@/types";
import { useState } from "react";
import { fetchProfile, fetchDiagnosis } from "@/lib/api";
import AuditorChat from "./AuditorChat";

const PROXY_BASE_URL = "http://localhost:8000/api/proxy_image?url=";

export default function AnalysisDashboard() {
    const [inputValue, setInputValue] = useState("");
    const [profile, setProfile] = useState<Profile | null>(null);
    const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);

    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [loadingStep, setLoadingStep] = useState("");
    const [error, setError] = useState("");

    const simulateProgress = () => {
        setProgress(10);
        setLoadingStep("Conectando con Instagram...");
        setTimeout(() => { setProgress(40); setLoadingStep("Descargando últimos posts..."); }, 1000);
        setTimeout(() => { setProgress(70); setLoadingStep("Analizando copies y estrategia..."); }, 3000);
        setTimeout(() => { setProgress(90); setLoadingStep("Generando diagnóstico IA..."); }, 5000);
    };

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        // Request permission on first interaction if default
        if (Notification.permission === "default") {
            Notification.requestPermission();
        }

        setLoading(true);
        setProgress(0);
        setProfile(null);
        setDiagnosis(null);
        setError("");
        document.title = "Analizando... | Strategist"; // Working state
        simulateProgress();

        try {
            // 1. Fetch Profile (Base Data)
            const p = await fetchProfile(inputValue);
            setProfile(p);

            // 2. Fetch Diagnosis (AI Analysis)
            try {
                const d = await fetchDiagnosis(p);
                setDiagnosis(d);

                // --- SUCCESS NOTIFICATIONS ---
                playSuccessSound();
                if (document.hidden && Notification.permission === "granted") {
                    new Notification("¡Análisis Completo! 🚀", {
                        body: `El diagnóstico de ${p.handle} está listo para revisar.`,
                        icon: "/favicon.ico" // Fallback icon
                    });
                }
                document.title = `✅ Listo: ${p.handle} | Strategist`;

            } catch (diagError) {
                console.error("Diagnosis Error:", diagError);
                setError("⚠️ Perfil cargado, pero el diagnóstico IA falló. Intenta de nuevo.");
                document.title = "⚠️ Error Parcial | Strategist";
            }

            setProgress(100);
        } catch (e) {
            console.error("Profile Error:", e);
            setError("Error: No se pudo acceder al perfil. Verifica que el usuario exista y sea público.");
            setProfile(null);
            document.title = "❌ Error | Strategist";
        } finally {
            setLoading(false);
        }
    };

    // Simple robust notification sound
    const playSuccessSound = () => {
        try {
            const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
            if (!AudioContext) return;

            const ctx = new AudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.connect(gain);
            gain.connect(ctx.destination);

            // "Check" sound: Short rising chirp (Success!)
            osc.frequency.setValueAtTime(400, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1000, ctx.currentTime + 0.15); // Quick rise

            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);

            osc.start();
            osc.stop(ctx.currentTime + 0.2);
        } catch (e) {
            console.error("Audio error", e);
        }
    };

    return (
        <div className="space-y-8">

            {/* --- Search & Progress --- */}
            <div className="bg-white rounded-xl p-6 card-shadow border border-slate-100">
                <label className="block text-sm font-medium text-slate-700 mb-2">Analizar Cuenta de Instagram</label>
                <form onSubmit={handleSearch} className="flex gap-3">
                    <div className="relative flex-1">
                        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">@</span>
                        <input
                            type="text"
                            placeholder="usuario"
                            className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg px-8 py-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                    >
                        {loading ? "Procesando..." : "Analizar"}
                    </button>
                </form>

                {loading && (
                    <div className="mt-6">
                        <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wide">
                            <span>{loadingStep}</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                            <div
                                className="bg-blue-500 h-full rounded-full transition-all duration-500 ease-out"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>
                    </div>
                )}

                {/* Error alert removed per user request */}
                {/* {error && (
                    <div className="mt-4 p-4 bg-red-50 text-red-600 border border-red-100 rounded-lg text-sm font-medium flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                        {error}
                    </div>
                )} */}
            </div>

            {profile && (
                <div className="animate-fade-in-up space-y-6">

                    {/* --- Profile Header Card --- */}
                    <div className="bg-white rounded-xl p-6 card-shadow border border-slate-100 flex flex-col md:flex-row items-center md:items-start gap-8">
                        <div className="shrink-0">
                            <img
                                src={`${PROXY_BASE_URL}${encodeURIComponent(profile.profile_pic_url)}`}
                                alt={profile.handle}
                                className="w-24 h-24 rounded-full border-4 border-slate-50 shadow-sm object-cover"
                                onError={(e) => { (e.target as HTMLImageElement).src = "https://ui-avatars.com/api/?background=random"; }}
                            />
                        </div>
                        <div className="flex-1 text-center md:text-left">
                            <div className="flex items-center justify-center md:justify-start gap-3 mb-1">
                                <h2 className="text-2xl font-bold text-slate-800">{profile.name}</h2>
                                <div className="flex items-center gap-2">
                                    <a
                                        href={`https://instagram.com/${profile.handle.replace('@', '')}`}
                                        target="_blank"
                                        className="text-slate-400 hover:text-blue-500 transition-colors"
                                    >
                                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" /></svg>
                                    </a>
                                    {profile.api_credits && (
                                        <span className="px-2 py-0.5 bg-slate-100 text-[10px] font-bold text-slate-500 rounded border border-slate-200 uppercase tracking-tighter">
                                            Créditos API: {profile.api_credits}
                                        </span>
                                    )}
                                </div>
                            </div>
                            <div className="text-slate-500 text-sm mb-4 font-medium">{profile.handle}</div>
                            <p className="text-slate-600 text-sm leading-relaxed max-w-3xl">{profile.bio}</p>
                        </div>

                        {/* Stats Grid */}
                        <div className="grid grid-cols-2 gap-x-8 gap-y-2 border-l border-slate-100 pl-8">
                            <div>
                                <div className="text-lg font-bold text-slate-800">{profile.stats.followers.toLocaleString()}</div>
                                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Seguidores</div>
                            </div>
                            <div>
                                <div className="text-lg font-bold text-slate-800">{profile.stats.total_posts.toLocaleString()}</div>
                                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Posts</div>
                            </div>
                            <div>
                                <div className="text-lg font-bold text-slate-800">{profile.stats.following.toLocaleString()}</div>
                                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Seguidos</div>
                            </div>
                            <div>
                                <div className="text-lg font-bold text-blue-600">{profile.stats.engagement_rate}%</div>
                                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Eng. Rate</div>
                            </div>
                        </div>
                    </div>

                    {/* --- Diagnosis Grid --- */}
                    {diagnosis && (
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                            {/* Main Insight */}
                            <div className="lg:col-span-3 bg-white rounded-xl p-8 card-shadow border border-slate-100 flex flex-col justify-between relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-10 -mt-10 z-0"></div>

                                <div className="relative z-10">
                                    <h3 className="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4">Diagnóstico Estratégico</h3>
                                    <p className="text-xl text-slate-700 font-light leading-relaxed mb-8">
                                        “{diagnosis.summary}”
                                    </p>

                                    <div className="space-y-3">
                                        {diagnosis.key_issues.map((issue, idx) => (
                                            <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-orange-50 border border-orange-100">
                                                <span className="text-orange-500 mt-0.5 text-lg">•</span>
                                                <span className="text-slate-700 text-sm font-medium">{issue}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>


                            {/* Recommendations Card */}
                            <div className="lg:col-span-3 bg-white rounded-xl p-8 card-shadow border border-slate-100 mt-6">
                                <h3 className="text-sm font-bold text-emerald-600 uppercase tracking-widest mb-6 flex items-center gap-2">
                                    <span>🚀</span> Plan de Acción para el 100%
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {diagnosis.recommendations?.map((rec, idx) => (
                                        <div key={idx} className="flex gap-4 p-4 rounded-lg bg-emerald-50/50 border border-emerald-100 hover:border-emerald-200 transition-colors">
                                            <div className="shrink-0 w-8 h-8 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center font-bold text-sm">
                                                {idx + 1}
                                            </div>
                                            <p className="text-slate-700 text-sm leading-relaxed font-medium">
                                                {rec}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>

                        </div>
                    )}

                    {/* --- Content Grid --- */}
                    <div className="bg-white rounded-xl p-6 card-shadow border border-slate-100">
                        <h3 className="text-sm font-bold text-slate-800 uppercase mb-6 flex items-center gap-2">
                            <span>📸</span> Galería Reciente
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {profile.posts.slice(0, 4).map((post) => (
                                <div key={post.id} className="group relative aspect-square bg-slate-100 rounded-lg overflow-hidden cursor-pointer shadow-sm hover:shadow-md transition-all">
                                    <img
                                        src={`${PROXY_BASE_URL}${encodeURIComponent(post.image_url || "")}`}
                                        alt="Instagram Post Content"
                                        className="w-full h-full object-cover"
                                        loading="lazy"
                                        onError={(e) => { (e.target as HTMLImageElement).src = "https://placehold.co/400x400?text=No+Image"; }}
                                    />
                                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
                                        <div className="text-white text-xs line-clamp-2 mb-2">{post.caption}</div>
                                        <div className="flex gap-3 text-xs font-medium text-white/90">
                                            <span>❤️ {post.likes}</span>
                                            <span>💬 {post.comments}</span>
                                        </div>
                                    </div>
                                    <div className="absolute top-2 right-2 px-2 py-0.5 bg-white/90 backdrop-blur rounded text-[10px] uppercase font-bold text-slate-800 shadow-sm">
                                        {post.type}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                </div>
            )}

            {profile && diagnosis && (
                <AuditorChat profile={profile} diagnosis={diagnosis} />
            )}
        </div>
    );
}
