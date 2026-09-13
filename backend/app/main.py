from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, situations, analyses, preferences

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST de IUnderstandYou: Agente de IA Personal para Apoyo a Decisiones Interpersonales",
    version="1.0.0"
)

# Configuración de CORS para integración con Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(situations.router)
app.include_router(analyses.router)
app.include_router(preferences.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de verificación de estado de la API."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "llm_provider": settings.LLM_PROVIDER
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)


