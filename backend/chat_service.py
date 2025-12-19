from models import Profile, Diagnosis, ChatMessage
import google.generativeai as genai
import os
import json

def generate_chat_response(message: str, history: list[ChatMessage], profile: Profile, diagnosis: Diagnosis) -> str:
    """
    Generates a response from the Auditor persona, debating the user.
    """
    # 1. Build Context String
    profile_summary = f"Handle: {profile.handle}, Bio: {profile.bio}, Followers: {profile.stats.followers}, ER: {profile.stats.engagement_rate}%"
    
    diagnosis_summary = f"Tone: {diagnosis.tone}, Summary: {diagnosis.summary}, Key Issues: {', '.join(diagnosis.key_issues)}"
    
    # 2. Build Conversation History for Prompt
    # We don't use the full chat session of the model object to keep it stateless/simple for HTTP
    history_text = ""
    for msg in history:
        role_label = "USUARIO" if msg.role == "user" else "AUDITOR"
        history_text += f"{role_label}: {msg.content}\n"

    # 3. Construct System Prompt
    prompt = f"""
    SISTEMA: Eres un Estratega Senior, un mentor "Sincero y Directo". Tu objetivo es ayudar al usuario a mejorar con honestidad radical pero profesionalismo absoluto.
    
    CONTEXTO DEL PERFIL:
    {profile_summary}
    
    TU DIAGNÓSTICO PREVIO:
    {diagnosis_summary}
    
    HISTORIAL DE CHAT:
    {history_text}
    
    USUARIO (Ahora): {message}
    
    INSTRUCCIONES:
    - Responde con sinceridad y profesionalismo.
    - FORMATO (CRÍTICO): Escribe en texto plano LIMPIO. NO uses NINGÚN símbolo de Markdown (como asteriscos *, guiones -, etc.).
    - ESPACIADO: Deja UN ESPACIO EN BLANCO (dos saltos de línea) entre cada párrafo. No pegues los párrafos.
    - Evita ser grosero o condescendiente. Tu valor es la claridad y la pulcritud.
    - Responde SÓLO con el mensaje de texto.
    """
    
    # 4. Generate
    # We reuse the model configuration from ai_service logic (assuming we can access the configured genai)
    # Re-initializing model here to avoid circular imports or global state complexity for this snippet
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    response = model.generate_content(prompt)
    return response.text
