import instaloader
import getpass

def interactive_login():
    print("=== 🔐 Instagram Authenticator ===")
    print("Para evitar bloqueos, necesitamos una sesión real.")
    print("RECOMENDACIÓN: Usa una cuenta secundaria/desechable, no tu principal.")
    
    username = input("Usuario IG: ")
    password = getpass.getpass("Contraseña: ")
    
    L = instaloader.Instaloader()
    
    try:
        print(f"Intentando login como {username}...")
        L.login(username, password)
        print("✅ Login Exitoso!")
        
        filename = f"session-{username}"
        L.save_session_to_file(filename=filename)
        print(f"💾 Sesión guardada en: {filename}")
        print("Ahora el scraper usará esta 'llave' para acceder.")
        
    except instaloader.TwoFactorAuthRequiredException:
        print("⚠️ Se requiere autenticación de dos pasos (2FA).")
        code = input("Código 2FA: ")
        L.two_factor_login(code)
        L.save_session_to_file(filename=f"session-{username}")
        print("✅ Login con 2FA Exitoso y guardado.")
        
    except Exception as e:
        print(f"❌ Error de Login: {e}")

if __name__ == "__main__":
    interactive_login()
