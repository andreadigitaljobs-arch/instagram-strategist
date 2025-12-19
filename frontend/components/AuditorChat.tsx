"use client";

import { useState, useRef, useEffect } from "react";
import { ChatMessage, Profile, Diagnosis } from "@/types";
import { sendChatMessage } from "@/lib/api";

interface AuditorChatProps {
    profile: Profile;
    diagnosis: Diagnosis;
}

export default function AuditorChat({ profile, diagnosis }: AuditorChatProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    // Auto-scroll to bottom
    const messagesEndRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isOpen]);

    // Initial greeting trigger
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            // Optional: Add a system greeting if desired, or just let the user start
            // For now, we'll let the user start or add a static greeting in UI
        }
    }, [isOpen, messages.length]);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMsg: ChatMessage = { role: "user", content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setLoading(true);

        try {
            const assistantMsg = await sendChatMessage(input, messages, profile, diagnosis);
            setMessages(prev => [...prev, assistantMsg]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Error de conexión. Intenta de nuevo." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* Floating Action Button */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    aria-label="Open Auditor Chat"
                    className="fixed bottom-8 right-8 bg-blue-600 hover:bg-blue-700 text-white font-bold p-4 rounded-full shadow-2xl transition-all hover:scale-105 z-50 flex items-center gap-2 animate-bounce-subtle"
                >
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                    <span>Debatir con el Auditor</span>
                </button>
            )}

            {/* Chat Drawer/Modal */}
            {isOpen && (
                <div className="fixed inset-0 z-50 flex justify-end md:p-4 pointer-events-none">
                    <div className="w-full md:w-[450px] bg-white h-full md:h-[600px] md:mt-auto md:rounded-2xl shadow-2xl border border-slate-200 flex flex-col pointer-events-auto transform transition-transform animate-slide-in-right">

                        {/* Header */}
                        <div className="p-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center rounded-t-2xl">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-xl">👨‍💻</div>
                                <div>
                                    <h3 className="font-bold text-slate-800">El Auditor</h3>
                                    <p className="text-xs text-slate-500 font-medium">Sincero y Directo</p>
                                </div>
                            </div>
                            <button onClick={() => setIsOpen(false)} aria-label="Close Chat" className="text-slate-400 hover:text-slate-600 p-2">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                            </button>
                        </div>

                        {/* Messages Area */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white/50">
                            {/* Static Intro */}
                            <div className="flex gap-3">
                                <div className="w-8 h-8 rounded-full bg-blue-100 flex-shrink-0 flex items-center justify-center text-sm">👨‍💻</div>
                                <div className="bg-slate-100 text-slate-700 p-3 rounded-2xl rounded-tl-none text-sm leading-relaxed max-w-[85%] whitespace-pre-wrap">
                                    He analizado tu perfil ({profile.handle}). He preparado un diagnóstico profesional sobre tu estrategia. ¿Quieres que profundicemos en algún punto específico o tienes alguna duda?
                                </div>
                            </div>

                            {messages.map((msg, idx) => (
                                <div key={idx} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                                    <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-sm ${msg.role === "user" ? "bg-indigo-100 text-indigo-700" : "bg-blue-100 text-blue-700"}`}>
                                        {msg.role === "user" ? "👤" : "👨‍💻"}
                                    </div>
                                    <div className={`p-3 rounded-2xl text-sm leading-relaxed max-w-[85%] whitespace-pre-wrap ${msg.role === "user"
                                        ? "bg-indigo-600 text-white rounded-tr-none"
                                        : "bg-slate-100 text-slate-700 rounded-tl-none"
                                        }`}>
                                        {msg.content}
                                    </div>
                                </div>
                            ))}

                            {loading && (
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded-full bg-blue-100 flex-shrink-0 flex items-center justify-center text-sm">👨‍💻</div>
                                    <div className="bg-slate-50 text-slate-400 p-3 rounded-2xl rounded-tl-none text-sm italic">
                                        Escribiendo...
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-4 bg-white border-t border-slate-100 rounded-b-2xl">
                            <form onSubmit={handleSend} className="flex gap-2">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Defiende tu estrategia..."
                                    className="flex-1 bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                                    disabled={loading}
                                />
                                <button
                                    type="submit"
                                    disabled={loading || !input.trim()}
                                    className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition-colors disabled:opacity-50"
                                >
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
                                </button>
                            </form>
                        </div>

                    </div>
                </div>
            )}
        </>
    );
}
