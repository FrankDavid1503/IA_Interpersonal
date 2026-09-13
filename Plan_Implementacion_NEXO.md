# Plan de Implementación — NEXO
## Agente de IA Personal para Apoyo a Decisiones Interpersonales

**Objetivo del documento:** servir como guía práctica para construir un prototipo funcional de NEXO. No busca ser un producto final; busca dejar una base técnica que funcione y que pueda ampliarse posteriormente.

---

# 1. Visión del proyecto

NEXO será un agente de IA personal que ayuda al usuario a analizar situaciones interpersonales antes de actuar.

Ejemplo:

> "Mi amigo está triste porque falleció su perrito y no sé qué decirle."

El sistema analiza la situación y devuelve:

- contexto detectado;
- emoción probable;
- nivel de sensibilidad/riesgo;
- alternativas de actuación;
- posibles consecuencias;
- recomendación;
- respuesta sugerida.

La IA **no decide por el usuario**. Funciona como apoyo para que el usuario pueda tomar una decisión más reflexiva.

---

# 2. Alcance del primer prototipo

## Funciones que SÍ se implementarán

1. Registro e inicio de sesión.
2. Perfil básico del usuario.
3. Registro de situaciones.
4. Análisis de una situación mediante IA.
5. Clasificación básica de contexto/emoción.
6. Generación de alternativas.
7. Evaluación cualitativa de consecuencias.
8. Recomendación de una alternativa.
9. Generación de una respuesta sugerida.
10. Historial de análisis del usuario.
11. Edición/eliminación de análisis propios.
12. Sistema básico de seguridad para detectar situaciones que requieren ayuda humana.

## Funciones que quedarán para una segunda etapa

- análisis de capturas de WhatsApp;
- audio;
- respuestas por voz;
- memoria avanzada;
- aprendizaje personalizado;
- aplicación móvil;
- integración directa con WhatsApp/Telegram;
- modelos propios entrenados con datos;
- agentes múltiples;
- despliegue completo en AWS.

Esto permite terminar primero una versión que realmente funcione.

---

# 3. Arquitectura general

```text
┌─────────────────────────────┐
│          FRONTEND           │
│       React / Next.js       │
│                             │
│ Login                       │
│ Dashboard                   │
│ Nueva situación             │
│ Resultado del análisis      │
│ Historial                   │
│ Perfil                      │
└──────────────┬──────────────┘
               │ HTTP / JSON
               ▼
┌─────────────────────────────┐
│          BACKEND            │
│       Python + FastAPI      │
│                             │
│ Auth                        │
│ Users                       │
│ Situations                  │
│ Analysis                    │
│ Recommendations             │
│ AI Agent                    │
│ Safety                      │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌────────────────┐
│ PostgreSQL   │  │     LLM API    │
│              │  │                │
│ usuarios     │  │ análisis       │
│ situaciones  │  │ alternativas   │
│ análisis     │  │ recomendación  │
│ alternativas │  │ respuesta      │
└──────────────┘  └────────────────┘
```

---

# 4. Stack tecnológico recomendado

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios o fetch
- React Hook Form

## Backend

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- JWT para autenticación
- Uvicorn

## Base de datos

**PostgreSQL**

Se recomienda PostgreSQL porque:

- es relacional;
- permite mantener integridad entre entidades;
- funciona bien con aplicaciones web;
- tiene buen soporte con Python;
- puede crecer posteriormente;
- permite incorporar funcionalidades vectoriales mediante PostgreSQL/pgvector en una etapa futura.

## IA

Inicialmente:

**LLM mediante API**

No se recomienda entrenar un modelo propio para el MVP.

La aplicación debe enviar el contexto al modelo y recibir una respuesta estructurada.

---

# 5. Diseño de la base de datos

Para el MVP se propone una base de datos de 7 tablas principales.

```text
users
  │
  ├──── situations
  │          │
  │          └──── analyses
  │                   │
  │                   ├──── analysis_emotions
  │                   └──── recommendations
  │
  └──── user_preferences

safety_events
```

---

# 6. Tabla users

Almacena los usuarios del sistema.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| name | VARCHAR | Nombre |
| email | VARCHAR | Correo |
| password_hash | VARCHAR | Contraseña cifrada/hash |
| created_at | TIMESTAMP | Fecha de registro |
| updated_at | TIMESTAMP | Última actualización |

### Reglas

- `id` como PK.
- `email` UNIQUE.
- Nunca almacenar contraseñas en texto plano.

---

# 7. Tabla user_preferences

Permite personalizar posteriormente las recomendaciones.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| user_id | UUID | Usuario |
| communication_style | VARCHAR | Estilo preferido |
| directness_level | VARCHAR | Directo, equilibrado, cuidadoso |
| preferred_response_length | VARCHAR | Corto, medio, largo |
| created_at | TIMESTAMP | Creación |
| updated_at | TIMESTAMP | Actualización |

Relación:

```text
users 1 ───── 1 user_preferences
```

---

# 8. Tabla situations

Guarda las situaciones introducidas por el usuario.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| user_id | UUID | Usuario propietario |
| input_text | TEXT | Situación descrita |
| relationship_type | VARCHAR | Amigo, familiar, compañero, etc. |
| objective | VARCHAR | Qué quiere lograr |
| created_at | TIMESTAMP | Fecha |

Ejemplo:

```text
input_text:
"Mi amigo está triste porque falleció su mascota."

relationship_type:
"amigo"

objective:
"Quiero saber qué decirle."
```

---

# 9. Tabla analyses

Representa el resultado general del análisis de IA.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| situation_id | UUID | Situación analizada |
| context_summary | TEXT | Resumen |
| detected_emotion | VARCHAR | Emoción principal |
| sensitivity_level | VARCHAR | low / medium / high |
| risk_level | VARCHAR | low / medium / high |
| recommendation | TEXT | Recomendación principal |
| suggested_response | TEXT | Respuesta sugerida |
| model_name | VARCHAR | Modelo utilizado |
| created_at | TIMESTAMP | Fecha |

Relación:

```text
situations 1 ───── N analyses
```

Guardar `model_name` permitirá saber con qué modelo se generó cada análisis.

---

# 10. Tabla analysis_emotions

Permite almacenar más de una emoción.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| analysis_id | UUID | Análisis |
| emotion | VARCHAR | Emoción |
| confidence | DECIMAL | Confianza |
| created_at | TIMESTAMP | Fecha |

Ejemplo:

```text
tristeza      0.91
soledad       0.62
preocupación  0.41
```

La confianza debe tratarse como una estimación del sistema, no como una medición psicológica.

---

# 11. Tabla recommendations

Guarda las alternativas propuestas por la IA.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| analysis_id | UUID | Análisis |
| title | VARCHAR | Nombre |
| description | TEXT | Explicación |
| benefit | TEXT | Posible beneficio |
| risk | TEXT | Posible riesgo |
| priority | INTEGER | Orden/prioridad |
| created_at | TIMESTAMP | Fecha |

Ejemplo:

```text
1. Escuchar
Beneficio: permite que la persona se exprese.
Riesgo: puede requerir tiempo y paciencia.

2. Ofrecer compañía
Beneficio: transmite apoyo.
Riesgo: la persona puede preferir estar sola.
```

---

# 12. Tabla safety_events

Registra únicamente eventos técnicos de seguridad necesarios para evaluar el funcionamiento del sistema.

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador |
| situation_id | UUID | Situación |
| risk_level | VARCHAR | Nivel detectado |
| category | VARCHAR | Categoría |
| action_taken | TEXT | Acción realizada |
| created_at | TIMESTAMP | Fecha |

No debe utilizarse para crear un historial innecesariamente detallado de información sensible.

---

# 13. Relaciones de la base de datos

```text
USER
 │
 ├────────────── USER_PREFERENCES
 │
 └────────────── SITUATIONS
                       │
                       └──────── ANALYSES
                                      │
                                      ├──── ANALYSIS_EMOTIONS
                                      │
                                      └──── RECOMMENDATIONS

SITUATIONS ─────────── SAFETY_EVENTS
```

---

# 14. Backend — estructura del proyecto

Se recomienda separar el backend por responsabilidades.

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── preference.py
│   │   ├── situation.py
│   │   ├── analysis.py
│   │   ├── emotion.py
│   │   ├── recommendation.py
│   │   └── safety_event.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── situation.py
│   │   ├── analysis.py
│   │   └── recommendation.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── situations.py
│   │   ├── analyses.py
│   │   └── preferences.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── situation_service.py
│   │   ├── analysis_service.py
│   │   ├── recommendation_service.py
│   │   └── safety_service.py
│   │
│   └── ai/
│       ├── agent.py
│       ├── prompts.py
│       ├── parser.py
│       └── safety.py
│
├── migrations/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

# 15. Responsabilidad de cada capa

## Models

Representan las tablas de PostgreSQL.

## Schemas

Definen qué información entra y sale de la API.

## Routers

Definen los endpoints.

## Services

Contienen la lógica de negocio.

## AI

Contiene la comunicación con el modelo de lenguaje.

Esta separación evita colocar toda la lógica en `main.py`.

---

# 16. Endpoints principales

## Autenticación

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

## Situaciones

```text
POST   /api/situations
GET    /api/situations
GET    /api/situations/{id}
DELETE /api/situations/{id}
```

## Análisis

```text
POST /api/situations/{id}/analyze
GET  /api/analyses/{id}
```

## Preferencias

```text
GET   /api/preferences
PUT   /api/preferences
```

---

# 17. Flujo principal del backend

Cuando el usuario solicita analizar una situación:

```text
POST /api/situations/{id}/analyze
             │
             ▼
      Verificar usuario
             │
             ▼
      Obtener situación
             │
             ▼
       Safety Check
             │
       ┌─────┴─────┐
       │           │
    Normal      Riesgo
       │           │
       ▼           ▼
    Agente IA   Respuesta
       │        de seguridad
       ▼
  Parsear JSON
       │
       ▼
Guardar Analysis
       │
       ├── Emotions
       │
       └── Recommendations
       │
       ▼
    Respuesta API
```

---

# 18. Diseño del agente de IA

El agente debe recibir información estructurada.

Ejemplo conceptual:

```text
Situación:
"Mi amigo está triste porque falleció su perro."

Relación:
"amigo"

Objetivo:
"saber cómo responder"

Preferencias:
"respuesta corta y natural"
```

La IA debe devolver una estructura definida, no texto libre.

Ejemplo:

```json
{
  "context_summary": "...",
  "detected_emotion": "tristeza",
  "sensitivity_level": "medium",
  "risk_level": "low",
  "recommendation": "...",
  "suggested_response": "...",
  "alternatives": [
    {
      "title": "Escuchar",
      "description": "...",
      "benefit": "...",
      "risk": "..."
    }
  ]
}
```

El backend valida este JSON antes de guardarlo.

---

# 19. Prompt del agente

El prompt debe definir claramente el rol:

```text
Eres NEXO, un agente de apoyo para decisiones interpersonales.

Tu función es ayudar al usuario a analizar situaciones sociales
y considerar diferentes alternativas antes de actuar.

No debes presentarte como psicólogo, terapeuta ni autoridad
sobre la vida del usuario.

No debes afirmar con certeza qué siente otra persona.
Utiliza expresiones como "podría estar sintiendo" cuando exista
incertidumbre.

Debes:
1. comprender el contexto;
2. identificar emociones probables;
3. identificar posibles riesgos;
4. generar alternativas;
5. explicar beneficios y posibles riesgos;
6. recomendar una alternativa razonable;
7. generar una respuesta que el usuario pueda adaptar.

Si detectas una situación de riesgo serio, prioriza la seguridad
y recomienda buscar ayuda humana apropiada.

Devuelve exclusivamente la estructura JSON solicitada.
```

El prompt real se debe versionar en el repositorio.

---

# 20. Frontend — estructura

```text
frontend/
│
├── app/
│   ├── login/
│   ├── register/
│   ├── dashboard/
│   ├── situation/
│   ├── analysis/
│   ├── history/
│   └── profile/
│
├── components/
│   ├── Navbar.tsx
│   ├── SituationForm.tsx
│   ├── AnalysisCard.tsx
│   ├── RecommendationCard.tsx
│   ├── EmotionBadge.tsx
│   └── SafetyAlert.tsx
│
├── services/
│   └── api.ts
│
├── types/
│   └── index.ts
│
└── README.md
```

---

# 21. Pantallas del frontend

## Pantalla 1 — Login

Campos:

- correo;
- contraseña.

Botón:

**Iniciar sesión**

---

## Pantalla 2 — Dashboard

Mostrar:

```text
Hola 👋

¿Qué situación quieres analizar?

[ Escribe aquí tu situación... ]

[ Analizar situación ]

--------------------------------

Análisis recientes

Situación 1
Situación 2
Situación 3
```

---

# 22. Pantalla de análisis

Esta será la pantalla más importante.

```text
┌──────────────────────────────────────┐
│ NEXO                                 │
│                                      │
│ Situación                            │
│ "Mi amigo está triste..."             │
│                                      │
│ Contexto detectado                   │
│ Pérdida / duelo                      │
│                                      │
│ Emoción probable                     │
│ Tristeza                             │
│                                      │
│ Recomendación                        │
│ Escuchar y acompañar                 │
│                                      │
│ Alternativas                         │
│                                      │
│ [Escuchar]                           │
│ [Ofrecer compañía]                   │
│ [Dar espacio]                        │
│                                      │
│ Respuesta sugerida                   │
│ "..."                                │
└──────────────────────────────────────┘
```

---

# 23. Historial

El usuario podrá visualizar:

```text
Mis análisis

12/09/2026
Discusión con un amigo

10/09/2026
Amigo preocupado

08/09/2026
Situación familiar
```

Al seleccionar uno:

```text
Situación
Análisis
Alternativas
Recomendación
Respuesta sugerida
```

---

# 24. Seguridad

El sistema debe diferenciar entre situaciones normales y situaciones que requieren intervención humana.

Ejemplo normal:

> "No sé cómo disculparme con mi amigo."

Puede proporcionar orientación.

Ejemplo de riesgo:

> Situación que indique peligro inmediato, violencia, amenazas u otra circunstancia grave.

En ese caso:

```text
⚠️ Esta situación puede requerir ayuda inmediata.

No es recomendable intentar resolverla únicamente
mediante este asistente.

Busca ayuda de una persona responsable o del servicio
de emergencia/profesional correspondiente a tu situación.
```

La IA no debe intentar sustituir a profesionales o servicios de emergencia.

---

# 25. Seguridad de datos

Implementar desde el inicio:

- HTTPS en producción.
- Contraseñas almacenadas mediante hash seguro.
- JWT con expiración.
- Validación de entrada.
- Control de acceso por usuario.
- Un usuario solo puede consultar sus propios análisis.
- Variables secretas en `.env`.
- `.env` incluido en `.gitignore`.
- `.env.example` sin claves reales.
- No guardar información innecesaria.

---

# 26. Desarrollo por etapas

## Etapa 1 — Preparación

Crear:

```text
backend/
frontend/
database/
docs/
```

Configurar Git.

Crear README.

Definir variables de entorno.

---

## Etapa 2 — Base de datos

1. Instalar PostgreSQL.
2. Crear base de datos `nexo_db`.
3. Configurar SQLAlchemy.
4. Crear modelos.
5. Configurar Alembic.
6. Crear migraciones.
7. Ejecutar migraciones.
8. Verificar relaciones.

**Resultado:** base de datos funcional.

---

## Etapa 3 — Backend básico

Implementar:

1. FastAPI.
2. Conexión PostgreSQL.
3. Modelos.
4. Schemas.
5. Registro.
6. Login.
7. JWT.
8. CRUD de situaciones.

**Resultado:** API funcionando sin IA.

---

## Etapa 4 — Integración de IA

Implementar:

1. Servicio de IA.
2. Prompt.
3. Entrada estructurada.
4. Respuesta JSON.
5. Validación mediante Pydantic.
6. Guardado de análisis.
7. Guardado de alternativas.
8. Control de errores.

**Resultado:** el backend puede analizar una situación.

---

## Etapa 5 — Frontend

Implementar:

1. Login.
2. Registro.
3. Dashboard.
4. Formulario de situación.
5. Pantalla de análisis.
6. Alternativas.
7. Respuesta sugerida.
8. Historial.
9. Perfil.

**Resultado:** aplicación usable de extremo a extremo.

---

## Etapa 6 — Seguridad y pruebas

Crear pruebas para:

- registro;
- login;
- autenticación;
- creación de situación;
- consulta de situación;
- análisis;
- permisos;
- respuestas inválidas de IA;
- situaciones de riesgo.

---

# 27. Orden recomendado de programación

No empezar por la IA.

El orden recomendado es:

```text
1. PostgreSQL
       ↓
2. Backend básico
       ↓
3. Autenticación
       ↓
4. Situaciones
       ↓
5. Frontend básico
       ↓
6. Integración IA
       ↓
7. Historial
       ↓
8. Seguridad
       ↓
9. Pruebas
       ↓
10. Mejoras
```

Esto permite comprobar que cada parte funciona antes de agregar complejidad.

---

# 28. Estructura final del proyecto

```text
NEXO/
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── types/
│   └── README.md
│
├── database/
│   ├── modelo_entidad_relacion.md
│   └── seeds/
│
├── docs/
│   ├── arquitectura.md
│   ├── decisiones_tecnicas.md
│   ├── agente_ia.md
│   ├── seguridad.md
│   ├── pruebas.md
│   └── api.md
│
├── .gitignore
└── README.md
```

---

# 29. Futuras mejoras

Una vez que el MVP funcione, se pueden incorporar:

### Multimodalidad

```text
Texto
Audio
Imagen
Captura de conversación
       ↓
     NEXO
```

### Memoria

El sistema podría recordar preferencias del usuario de forma controlada.

### RAG

Agregar una base de conocimiento con información confiable para determinados temas.

### pgvector

PostgreSQL podría utilizarse posteriormente para almacenar embeddings y realizar búsquedas semánticas.

### Agente con herramientas

El agente podría consultar:

- memoria personal;
- historial;
- base de conocimiento;
- reglas de seguridad.

---

# 30. Resultado esperado

El objetivo inicial NO es crear una IA perfecta.

El objetivo es conseguir un sistema donde:

```text
Usuario
   ↓
Describe una situación
   ↓
Frontend
   ↓
Backend
   ↓
Agente IA
   ↓
Análisis estructurado
   ↓
PostgreSQL
   ↓
Frontend
   ↓
Usuario recibe:
- contexto
- emociones probables
- alternativas
- consecuencias
- recomendación
- respuesta sugerida
```

Si este flujo funciona correctamente, el proyecto ya tendrá una base sólida y demostrable.

---

# 31. Primera versión mínima viable

La primera versión debería conseguir exactamente esto:

> Un usuario inicia sesión, escribe una situación interpersonal, NEXO analiza el contexto mediante IA, genera tres alternativas con beneficios y riesgos, recomienda una opción, genera una respuesta sugerida y guarda el análisis en PostgreSQL para que el usuario pueda consultarlo posteriormente.

Ese será el **MVP funcional**.

A partir de este punto se pueden añadir memoria, multimodalidad, voz, RAG, agentes especializados y despliegue en AWS sin tener que rehacer toda la arquitectura.

---

# 32. Próximo paso de implementación

El siguiente paso recomendado es comenzar por:

**FASE 1: crear el repositorio y levantar PostgreSQL + Backend FastAPI.**

Después se debe crear la primera migración con:

```text
users
user_preferences
situations
analyses
analysis_emotions
recommendations
safety_events
```

Una vez que PostgreSQL y FastAPI estén conectados correctamente, se continúa con autenticación y posteriormente con el agente de IA.

