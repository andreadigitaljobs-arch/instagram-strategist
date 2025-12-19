export type PostType = "static" | "reel" | "carousel";

export type ContentCategory =
    | "Educativo"
    | "Documental/Día a día"
    | "Opinión/Criterio"
    | "Venta directa"
    | "Marca personal"
    | "Neutro/Relleno"
    | "Desconocido";

export interface Post {
    id: string;
    type: PostType;
    caption: string;
    likes: number;
    comments: number;
    category: ContentCategory;
    image_url?: string;
}

export interface ProfileStats {
    total_posts: number;
    followers: number;
    following: number;
    engagement_rate: number;
    posts_per_week: number;
}

export interface Profile {
    handle: string;
    name: string;
    bio: string;
    profile_pic_url: string;
    stats: ProfileStats;
    posts: Post[];
    api_credits?: string;
}

export interface Diagnosis {
    summary: string;
    tone: string;
    score: number;
    key_issues: string[];
    viral_potential: string;
    difficulty_level?: string;
    structure_blueprint?: string;
    psychological_trigger?: string;
    production_guide?: {
        difficulty: string;
        explanation: string;
        equipment: string[];
        tips: string;
        shooting_plan?: {
            angles: string[];
            lighting: string;
            audio: string;
        };
    };
    recommendations: string[];
    tags?: string[];
    viral_mechanics?: {
        hook: string;
        retention: string;
        cta: string;
    };
    timeline?: {
        time: string;
        event: string;
        why_it_works: string;
    }[];
    missed_opportunities?: string[];
}

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}
