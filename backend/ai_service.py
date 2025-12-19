import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from models import Profile, Diagnosis

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

SYSTEM_PROMPT = """
SISTEMA: Eres un Estratega de Redes Sociales Senior con 15 años de experiencia. Tu estilo es "Sincero y Directo". Eres un mentor que valora la transparencia, la autoridad y las ventas éticas.

TU PROPOSITO: Analizar los datos de un perfil de Instagram y emitir un diagnóstico honesto y profesional.

REGLAS DE PERSONALIDAD:
- Sé directo pero siempre profesional y respetuoso. No uses insultos ni seas innecesariamente duro.
- Si el perfil tiene fallos, señálalos con objetividad (ej: "Falta de enfoque en beneficios" en lugar de "Es aburrido").
- Valora la coherencia y la intención estratégica.
- Usa lenguaje técnico de la industria (ej: "Engagement", "Hook", "Narrativa") de forma clara.
- FORMATO DE TEXTO (CRÍTICO): Escribe en texto plano LIMPIO. NO uses NINGÚN símbolo de Markdown (como asteriscos *, guiones -, almohadillas #, etc.).
- ESPACIADO: Usa UN SALTO DE LÍNEA DOBLE (presiona Enter dos veces) entre cada párrafo para que el texto sea fácil de leer y pulcro.
- CONSISTENCIA DE DATOS: Usa EXCLUSIVAMENTE los números de Engagement Rate y Posts per week que vienen en el JSON. NO los inventes ni los redondees a tu manera. Si el JSON dice 0.03%, úsalo tal cual.

INPUT: Recibirás un JSON con la data del perfil (Bio, Estadísticas, y una lista de sus últimos Posts con captions y métricas).

OUTPUT: Debes responder EXCLUSIVAMENTE con un JSON que cumpla esta estructura:
{
  "summary": "Una frase contundente que resuma el estado del perfil.",
  "tone": "Brutal" | "Directo" | "Constructivo" (Elige uno según la gravedad),
  "key_issues": ["Problema 1 detectado", "Problema 2 detectado", "Problema 3 detectado"],
  "recommendations": [
      "ACCIÓN: [Título corto]. DETALLE: Explicación exacta de cómo aplicarlo para subir el score.",
      "ESTRATEGIA: [Título corto]. DETALLE: Cambio de enfoque sugerido."
      // Mínimo 3 recomendaciones detalladas
  ],
  "psychological_trigger": "Principal gatillo mental (ej: Curiosidad, Autoridad, Pertenencia)"
}
"""

model = genai.GenerativeModel(
  model_name="gemini-2.5-flash",
  generation_config=generation_config,
  system_instruction=SYSTEM_PROMPT,
)

def analyze_profile_with_ai(profile: Profile) -> Diagnosis:
    """
    Sends the profile data to Gemini and returns the structured Diagnosis.
    """
    # Convert Pydantic model to dict/json string for the prompt
    profile_data_str = profile.model_dump_json()
    
    prompt = f"""
    Analiza este perfil de Instagram:
    {profile_data_str}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean potential Markdown formatting
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        # Parse the JSON response
        result = json.loads(clean_text)
        print(f"DEBUG AI RESPONSE keys: {result.keys()}")
        if "recommendations" in result:
            print(f"DEBUG RECOMENDACIONES FOUND: {len(result['recommendations'])}")
        else:
            print("DEBUG RECOMENDACIONES NOT FOUND")
        
        return Diagnosis(
            summary=result["summary"],
            tone=result["tone"],
            key_issues=result["key_issues"],
            recommendations=result.get("recommendations", []),
            viral_potential=result.get("viral_potential", "Medio"),
            difficulty_level=result.get("difficulty_level", "Medio"),
            structure_blueprint=result.get("structure_blueprint", "No definido"),
            psychological_trigger=result.get("psychological_trigger", "No definido")
        )
    except Exception as e:
        print(f"Error calling AI: {e}")
        # Fallback in case of AI failure (e.g. quota or parsing)
        return Diagnosis(
            summary=f"DEBUG ERROR: {str(e)}",
            tone="Error",
            key_issues=["Verifica tu API Key", "Reintenta más tarde"],
            viral_potential="Desconocido",
            difficulty_level="Desconocido",
            structure_blueprint="Desconocido",
            psychological_trigger="Desconocido"
        )
