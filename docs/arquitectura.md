# Arquitectura del Sistema NEXO

## Resumen del Flujo General

1. **Usuario:** Ingresa a través de la aplicación Web (Next.js 14).
2. **Frontend:** Autentica mediante JWT contra FastAPI y envía situaciones interpersonales en formato JSON.
3. **Backend (FastAPI):**
   - Autentica el token JWT del usuario.
   - Aplica el **Filtro de Seguridad (Pre-LLM)** en `app/ai/safety.py`.
   - Si no hay riesgo elevado, invoca la capa de IA (`app/ai/agent.py`).
   - Parsea y valida el JSON de respuesta contra esquemas Pydantic (`app/ai/parser.py`).
   - Guarda la situación, el análisis, las emociones y recomendaciones en la base de datos PostgreSQL.
4. **Base de Datos (PostgreSQL):** Almacena de manera relacional usuarios, preferencias, situaciones, análisis y eventos de seguridad.
