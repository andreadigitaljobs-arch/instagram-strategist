import { Profile, Diagnosis } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export async function fetchProfile(handle: string): Promise<Profile> {
    const res = await fetch(`${API_BASE_URL}/profile/${handle}`);
    if (!res.ok) {
        throw new Error("Failed to fetch profile");
    }
    return res.json();
}

export async function fetchDiagnosis(profile: Profile): Promise<Diagnosis> {
    const res = await fetch(`${API_BASE_URL}/diagnose`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(profile),
    });

    if (!res.ok) {
        const errText = await res.text();
        console.error(`Diagnosis fetch failed: ${res.status} ${res.statusText}`, errText);
        throw new Error(`Failed to fetch diagnosis: ${res.status}`);
    }
    return res.json();
}

export async function sendChatMessage(
    message: string,
    history: { role: "user" | "assistant"; content: string }[],
    profile: Profile,
    diagnosis: Diagnosis
): Promise<{ role: "assistant"; content: string }> {
    const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message,
            history,
            profile_context: profile,
            diagnosis_context: diagnosis
        }),
    });

    if (!res.ok) {
        throw new Error("Chat request failed");
    }
    return res.json();
}

export async function analyzeVideo(url: string): Promise<Diagnosis> {
    const res = await fetch(`${API_BASE_URL}/analyze_video`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Error en el análisis. Verifica el link.");
    }

    return res.json();
}
