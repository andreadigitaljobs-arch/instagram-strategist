# Instagram Strategist - Guía de Despliegue Web 🚀

Esta guía te ayudará a subir tu aplicación a la web utilizando **Render** (Backend) y **Vercel** (Frontend).

---

## 1. Backend (FastAPI) - Despliegue en Render

1. **GitHub:** Sube la carpeta `/backend` a un repositorio de GitHub (o todo el proyecto).
2. **Registro:** Ve a [Render.com](https://render.com/) y crea una cuenta.
3. **Nuevo Servicio:** Haz clic en **New +** -> **Web Service**.
4. **Conectar:** Conecta tu repositorio de GitHub.
5. **Configuración:**
   - **Root Directory:** `backend`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT` (O deja que lea el `Procfile`).
6. **Variables de Entorno (Environment):** Añade las siguientes:
   - `RAPIDAPI_KEY`: Tu llave de RapidAPI.
   - `RAPIDAPI_HOST`: `instagram-best-experience.p.rapidapi.com`
   - `GOOGLE_API_KEY`: Tu llave de Gemini AI.
   - `ALLOWED_ORIGINS`: El URL que te dé Vercel (ej: `https://tu-app.vercel.app`).

---

## 2. Frontend (Next.js) - Despliegue en Vercel

1. **Registro:** Ve a [Vercel.com](https://vercel.com/) y conecta tu GitHub.
2. **Importar:** Selecciona tu repositorio.
3. **Configuración:**
   - **Framework Preset:** `Next.js`
   - **Root Directory:** `frontend`
4. **Variables de Entorno:**
   - `NEXT_PUBLIC_API_URL`: El URL que te dio Render (ej: `https://tu-backend.onrender.com/api`).
5. **Deploy:** Haz clic en **Deploy**.

---

## 3. Notas Importantes

- **CORS:** Si la web no puede hablar con el backend, asegúrate de que el URL de Vercel esté en la variable `ALLOWED_ORIGINS` del backend en Render.
- **Créditos:** Recuerda que el scraper consume créditos de tu cuenta de RapidAPI. El Auditor y el Laboratorio de Video usan tu Google API Key.
