# NEXO — Agente de IA Personal para Apoyo a Decisiones Interpersonales

NEXO es una plataforma inteligente orientada al análisis y la reflexión de situaciones interpersonales complejas. Ayuda al usuario a evaluar contextos sociales, emociones involucradas, niveles de sensibilidad, alternativas de acción y respuestas sugeridas antes de actuar.

> **Nota:** NEXO funciona como una herramienta de apoyo reflexivo y no reemplaza el criterio del usuario ni constituye un servicio de asistencia terapéutica o profesional.

---

## 🏗️ Arquitectura General

- **Backend:** Python 3.10+ / FastAPI / SQLAlchemy / Alembic / Pydantic
- **Frontend:** Next.js 14 (App Router) / React / TypeScript / Tailwind CSS
- **Base de Datos:** PostgreSQL
- **IA / LLM:** Integración estructurada mediante Pydantic (OpenAI / Gemini / Mocks de desarrollo)

---

## 📁 Estructura del Repositorio

```text
IA_Interpersonal/
├── backend/          # API REST en FastAPI, servicios de IA, modelos y rutas
├── frontend/         # Aplicación Web Next.js 14
├── database/         # Documentación de ERD y scripts de semillas (seeds)
├── docs/             # Documentación técnica y especificaciones de arquitectura
├── .gitignore        # Exclusiones de control de versiones
└── README.md         # Documento principal del proyecto
```

---

## 🚀 Guía de Inicio Rápido

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --port 8000
```

Accede a la documentación interactiva OpenAPI en: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Accede a la aplicación en: [http://localhost:3000](http://localhost:3000)

---

## 📋 Estado del Desarrollo (Sprints)

- [x] **Sprint 0:** Preparación de repositorio y estructura inicial.
- [ ] **Sprint 1:** PostgreSQL, modelos SQLAlchemy y migraciones Alembic.
- [ ] **Sprint 2:** FastAPI y Autenticación con JWT.
- [ ] **Sprint 3:** CRUD de Situaciones e Historial Base.
- [ ] **Sprint 4:** Capa de Seguridad y Filtro de Riesgo (Pre-LLM).
- [ ] **Sprint 5:** Integración del Agente de IA y JSON Estructurado.
- [ ] **Sprint 6:** Frontend Base y Estado de Autenticación.
- [ ] **Sprint 7:** Formulario de Situación y Pantalla de Análisis.
- [ ] **Sprint 8:** Historial y Preferencias de Usuario.
- [ ] **Sprint 9:** Pruebas End-to-End, Seguridad y UX.
- [ ] **Sprint 10:** Documentación y Demo Final.
