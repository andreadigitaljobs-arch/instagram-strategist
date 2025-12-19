import yt_dlp
import google.generativeai as genai
import os
import time
from models import Diagnosis
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found in env.")
genai.configure(api_key=api_key)

def download_video(url: str) -> str:
    """
    Downloads a video from a URL (Instagram, TikTok, YouTube) using yt-dlp.
    Returns the local file path.
    """
    # Create temp dir if not exists (absolute path for production)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(base_dir, "temp_videos")
    os.makedirs(temp_dir, exist_ok=True)
    
    timestamp = int(time.time())
    output_template = os.path.join(temp_dir, f"video_{timestamp}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[ext=mp4]/best', # Prefer mp4
        'quiet': True,
        'max_filesize': 50 * 1024 * 1024, # Max 50MB to avoid huge uploads
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise ValueError(f"No se pudo descargar el video. Verifica el link. Error: {e}")

def analyze_video_content(video_path: str) -> Diagnosis:
    """
    Uploads video to Gemini and requests a Viral DNA analysis.
    """
    print(f"Uploading video {video_path} to Gemini...")
    
    try:
        # 1. Upload File
        video_file = genai.upload_file(path=video_path)
        
        # 2. Wait for processing (Gemini needs time to process video)
        while video_file.state.name == "PROCESSING":
            print("Processing video...", end='.', flush=True)
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
            
        if video_file.state.name == "FAILED":
            raise ValueError("Gemini falló al procesar el video.")
            
        print("Video ready. Generating analysis...")
        
        # 3. Generate Content
        from ai_service import model # reusing the configured model (2.5 flash)
        
        prompt = """
    ACTÚA COMO: Un Ingeniero Inverso de Viralidad y Psicólogo del Consumidor experto en Short-Form Content (Reels/TikTok).
    IMPORTANTE: RESPONDE ÚNICAMENTE EN ESPAÑOL. NO ISSUES RESPONSES IN PORTUGUESE OR ENGLISH.
    
    OBJETIVO: Deconstruir este video que YA ES EXITOSO (o tiene intención de serlo) para entender su "ADN Viral".
    NO des consejos básicos de mejora. Tu trabajo es EXPLICAR POR QUÉ FUNCIONA (o por qué está diseñado para funcionar).
    Analiza la psicología, la edición, los formatos y la estructura.

    TAREA 1: CLASIFICACIÓN (TAGS)
    Identifica el Estilo y Formato. Usa etiquetas como:
    - Estilo: "Cinematográfico" (Pro), "Orgánico" (iPhone/Raw), "Híbrido/Mixto" (Mezcla).
    - Edición: "Dinámica" (Muchos cortes), "Minimalista", "Solo Subtítulos", "VFX Heavy".
    - Formato: "Storytelling", "Sketck", "Tutorial Rápido", "Showcase", "POV".

    TAREA 2: MECÁNICA VIRAL (EL PORQUÉ)
    - Gancho (Hook): ¿Qué pasa exactamente en los primeros 3 segundos? ¿Es visual, auditivo o textual?
    - Retención: ¿Qué trucos de edición o narrativa mantienen la atención?
    - CTA (Call to Action): ¿Cómo cierra?

    TAREA 3: LÍNEA DE TIEMPO (TIMELINE)
    Desglosa momentos clave y la psicología detrás de ellos.

    TAREA 4: CRÍTICA DE ESCALABILIDAD (¿POR QUÉ NO 1 MILLÓN?)
    Si este video tuvo 50k vistas pero no 1M, ¿qué falló?
    Identifica "Fricciones" o "Frenos".
    Ejemplos: "Muy nicho", "Faltó polémica", "Gancho visual débil", "Duración excesiva".

    TAREA 5: GUÍA DE PRODUCCIÓN (El "Cómo se hizo")
    No solo digas la dificultad, explica QUÉ SE NECESITA.
    - Dificultad: "Bajo", "Medio", "Alto".
    - Explicación: ¿Por qué es esa dificultad? (ej: "Solo requiere hablar a cámara" vs "Requiere transiciones complejas").
    - Equipo: Lista de herramientas estimadas (ej: "Celular, Trípode, Luz de ventana", "Micrófono Solapa", "Premiere Pro").
    - Tips de Grabación: Cómo lograr ese look (ej: "Graba a contraluz", "Usa la cámara trasera").

    TAREA 6: BLUEPRINT (La Fórmula)
    Extrae la estructura abstracta como una fórmula matemática simple.
    Ejemplo: "[Pregunta Retórica] + [Historia Personal] + [Dato Duro] + [CTA]"

    TAREA 7: TRIGGER PSICOLÓGICO
    Identifica la emoción primaria que mueve el video.
    Ejemplos: "Curiosidad", "Validación", "Miedo (FOMO)", "Humor/Alivio".

    OUTPUT JSON (Estrictamente este formato):
    {
      "summary": "Análisis profundo de la ingeniería del video.",
      "tone": "Analítico",
      "viral_potential": "Explosivo 🧨", 
      "difficulty_level": "Bajo (Easy Win) ⚡",
      "production_guide": {
        "difficulty": "Bajo ⚡",
        "explanation": "Es un video orgánico sin cortes complejos.",
        "equipment": ["Celular (Cámara Trasera)", "Luz Natural"],
        "tips": "Mantén el celular estático y habla rápido."
      },
      "structure_blueprint": "[Gancho] + [Historia] + [Cierre]",
      "psychological_trigger": "Curiosidad Intelectual",
      "key_issues": [], 
      "tags": ["Cinematográfico", "Storytelling", "Edición Dinámica"], 
      "tags": ["Cinematográfico", "Storytelling", "Edición Dinámica"],
      "viral_mechanics": {
        "hook": "Análisis del gancho...",
        "retention": "Análisis de la retención...",
        "cta": "Análisis del cierre..."
      },
      "timeline": [
        {"time": "0-3s", "event": "El Gancho", "why_it_works": "Usa un patrón de interrupción visual..."},
        {"time": "3-15s", "event": "Desarrollo", "why_it_works": "Mantiene el ritmo con cortes cada 2s..."}
      ],
      "missed_opportunities": [
        "Falta de Universalidad: El tema es demasiado específico para Portugal.",
        "Gancho Lento: El primer segundo es silencio, debería empezar con acción."
      ],
      "recommendations": ["Tip avanzado 1", "Tip avanzado 2"] 
    }
    """
    
        # Call Gemini with the video
        print("Invoking Gemini generation...")
        response = model.generate_content([video_file, prompt])
        
        # Cleanup video from cloud if possible (optional, but good practice)
        # try:
        #     genai.delete_file(video_file.name)
        # except:
        #     pass

        # Cleanup local file
        try:
            os.remove(video_path)
        except:
            pass
            
        import json
        text_response = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text_response)
        
        return Diagnosis(
            summary=result.get("summary", "Sin resumen"),
            tone=result.get("tone", "Neutro"),
            key_issues=result.get("key_issues", []),
            recommendations=result.get("recommendations", []),
            viral_potential=result.get("viral_potential", "Bajo 📉"),
            difficulty_level=result.get("difficulty_level", "Medio 🛠️"),
            production_guide=result.get("production_guide", {}),
            structure_blueprint=result.get("structure_blueprint", "No definido"),
            psychological_trigger=result.get("psychological_trigger", "No definido"),
            tags=result.get("tags", []),
            viral_mechanics=result.get("viral_mechanics", {}),
            timeline=result.get("timeline", []),
            missed_opportunities=result.get("missed_opportunities", [])
        )

    except Exception as e:
        print(f"Error analyzing video: {e}")
        # Cleanup local file on error
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except:
                pass
        
        return Diagnosis(
            summary=f"Error en el análisis: {str(e)}",
            tone="Error",
            key_issues=["Fallo técnico"],
            viral_potential="Error ⚠️",
            recommendations=[],
            tags=[],
            viral_mechanics={"hook": "Error", "retention": "Error", "cta": "Error"},
            timeline=[]
        )
