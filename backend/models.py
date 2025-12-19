from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class PostType(str, Enum):
    STATIC = "static"
    REEL = "reel"
    CAROUSEL = "carousel"

class ContentCategory(str, Enum):
    EDUCATIONAL = "Educativo"
    DOCUMENTARY = "Documental/Día a día"
    OPINION = "Opinión/Criterio"
    SALES = "Venta directa"
    PERSONAL_BRAND = "Marca personal"
    FILLER = "Neutro/Relleno"
    UNKNOWN = "Desconocido"

class Post(BaseModel):
    id: str
    type: PostType
    caption: str
    likes: int
    comments: int
    # En un futuro esto vendrá de un análisis de IA
    category: ContentCategory = ContentCategory.UNKNOWN
    # URL simulada para el MVP
    image_url: Optional[str] = None

class ProfileStats(BaseModel):
    total_posts: int
    followers: int
    following: int
    # Métricas calculadas
    engagement_rate: float
    posts_per_week: float

class Profile(BaseModel):
    handle: str
    name: str
    bio: str
    profile_pic_url: str
    stats: ProfileStats
    posts: List[Post]
    api_credits: Optional[str] = None

class Diagnosis(BaseModel):
    summary: str
    tone: str # "Brutal", "Constructivo"
    key_issues: List[str]
    recommendations: List[str] = []
    viral_potential: str # Keep for compatibility or remove later if unused
    difficulty_level: str # "Bajo (Easy)", "Medio", "Alto (Pro)"
    structure_blueprint: str # "[Hook] + [Story] + [CTA]"
    psychological_trigger: str # "Curiosidad", "FOMO", "Identidad"
    production_guide: dict = {} # { "difficulty": "Media", "explanation": "...", "equipment": ["..."], "tips": "..." }
    
    # New fields for Viral Video Lab
    tags: list[str] = [] # "Cinematográfico", "Orgánico", "Edición Dinámica", etc.
    viral_mechanics: dict = {} # { "hook": "...", "retention": "...", "cta": "..." }
    timeline: list[dict] = [] # [ { "time": "0-3s", "event": "Gancho Visual" }, ... ]
    missed_opportunities: list[str] = [] # "¿Por qué no llegó al millón?"

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]
    profile_context: Profile
    diagnosis_context: Diagnosis

