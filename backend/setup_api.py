import os

def setup_rapidapi():
    print("=== 🚀 Configuración de Instagram API (RapidAPI) ===")
    print("Necesitamos tu 'Key' para poder analizar perfiles reales sin bloqueos.")
    print("\nINSTRUCCIONES SIMPLES:")
    print("1. Ve a: https://rapidapi.com/auth/sign-up (Si no tienes cuenta)")
    print("2. En tu búsqueda (ya lo tienes en pantalla), elige el PRIMERO: 'Instagram best experience'")
    print("   O usa este link: https://rapidapi.com/lobster/api/instagram-best-experience")
    print("3. Dale al botón azul 'Subscribe to Test' (Plan Basic Free - $0)")
    print("4. Copia el código 'X-RapidAPI-Key'")
    print("\n-------------------------------------------------------")
    
    key = input("PEGAR TU KEY AQUÍ: ").strip()
    
    if len(key) < 10:
        print("❌ Error: Esa clave parece demasiado corta. Inténtalo de nuevo.")
        return

    env_content = f"""RAPIDAPI_KEY={key}
RAPIDAPI_HOST=instagram-best-experience.p.rapidapi.com
# GEMINI_API_KEY= (Ya la tienes configurada en el sistema)
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
        
    print("\n✅ ¡LISTO! Configuración guardada.")
    print("Ahora reinicia el servidor backend para aplicar los cambios.")

if __name__ == "__main__":
    setup_rapidapi()
