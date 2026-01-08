import requests
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
    Downloads a video using 'Instagram Video & Image Downloader' via RapidAPI.
    Replaces yt-dlp (blocked on Render).
    """
    # 1. Prepare Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(base_dir, "temp_videos")
    os.makedirs(temp_dir, exist_ok=True)
    
    timestamp = int(time.time())
    output_path = os.path.join(temp_dir, f"video_{timestamp}.mp4")

    # 2. Call RapidAPI to get Download URL
    # Using 'Instagram Scraper 2022' (Stable & Popular)
    DOWNLOADER_HOST = "instagram-scraper-2022.p.rapidapi.com"
    API_KEY = os.getenv("RAPIDAPI_KEY") 
    
    if not API_KEY:
        raise ValueError("Falta la RAPIDAPI_KEY en las variables de entorno.")

    print(f"Resolving video URL via RapidAPI ({DOWNLOADER_HOST})...")
    
    try:
        # endpoint: /ig/post_info/?shortcode={shortcode} OR /ig/post_details/?url={url} depends on api
        # Research shows this API works with shortcodes often.
        # But let's check input 'url'.
        # We need to extract shortcode from URL if API requires it.
        # However, many have a simple url endpoint.
        # Let's try to extract shortcode just in case.
        
        # Extract shortcode from URL
        # URL format: https://www.instagram.com/reel/ShortCode/
        shortcode = url.split("/reel/")[-1].split("/")[0]
        if not shortcode:
             shortcode = url.split("/p/")[-1].split("/")[0]
             
        api_url = f"https://{DOWNLOADER_HOST}/ig/post_info/"
        querystring = {"shortcode": shortcode}
        
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": DOWNLOADER_HOST
        }
        
        # Call API
        response = requests.get(api_url, headers=headers, params=querystring)
        
        if response.status_code == 403:
             raise ValueError("⚠️ Falta Suscripción: Debes suscribirte GRATIS a 'Instagram Scraper 2022' en RapidAPI.")
        
        if response.status_code == 429:
             raise ValueError("⚠️ Límite Excedido: Se acabaron los créditos de descarga en RapidAPI.")

        if response.status_code != 200:
             raise ValueError(f"Error Downloader API ({response.status_code}): {response.text}")

        data = response.json()
        
        # Extract MP4 URL for 'Instagram Scraper 2022'
        download_url = None
        
        # Structure often: data -> video_url OR items[0] -> video_versions
        if "video_url" in data:
             download_url = data["video_url"]
        elif "url" in data:
             download_url = data["url"]
        elif "data" in data:
             if "video_url" in data["data"]:
                 download_url = data["data"]["video_url"]
             elif "video_versions" in data["data"]:
                 download_url = data["data"]["video_versions"][0]["url"]
                 
        if not download_url:
            # Fallback inspection
            print(f"DEBUG: API Data keys: {data.keys() if isinstance(data, dict) else 'List'}")
            raise ValueError("No se encontró el link de descarga en la respuesta de la API.")
            
        print(f"Video URL resolved: {download_url[:50]}...")

        # 3. Download the actual file content
        print("Downloading video bytes...")
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
                    
        print(f"Video saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error in download_video: {e}")
        raise ValueError(f"Error de descarga: {str(e)}")

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
