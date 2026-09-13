import re
from app.core.config import settings
from app.ai.prompts import NEXO_SYSTEM_PROMPT, build_user_prompt
from app.ai.parser import AIAnalysisSchema, EmotionDetail, AlternativeDetail, parse_and_validate_llm_json


def compute_dynamic_sensitivity(text: str) -> str:
    """Determina dinámicamente el nivel de sensibilidad basado en el impacto emocional del texto."""
    text_lower = text.lower()
    high_keywords = [
        "falleció", "fallecido", "muerte", "murió", "luto", "duelo", "grave", 
        "enfermedad", "separación", "divorcio", "llorando", "desesperad", "crisis", "perdió"
    ]
    medium_keywords = [
        "triste", "preocupad", "molest", "enojad", "malentendido", "estrés", "estres",
        "miedo", "discusión", "discutir", "tensión", "distancia", "abrumad", "examen", "exámenes"
    ]
    
    if any(k in text_lower for k in high_keywords):
        return "high"
    elif any(k in text_lower for k in medium_keywords):
        return "medium"
    return "low"


def compute_dynamic_risk(text: str) -> str:
    """Determina dinámicamente el nivel de riesgo en función del nivel de conflicto detectado."""
    text_lower = text.lower()
    high_risk_keywords = ["pelea fuerte", "peleamos feo", "gritos", "amenaz", "traición", "infidelidad", "odio", "nunca más"]
    medium_risk_keywords = ["discusión", "no me habla", "bloqueó", "molesto", "enojado", "malentendido", "pelea"]
    
    if any(k in text_lower for k in high_risk_keywords):
        return "high"
    elif any(k in text_lower for k in medium_risk_keywords):
        return "medium"
    return "low"


def generate_contextual_mock_analysis(input_text: str, relationship_type: str, objective: str) -> AIAnalysisSchema:
    """Motor analítico contextual que adapta el 100% de la salida de la IA al tipo de vínculo seleccionado (Familiar, Amigo, Trabajo/Estudio, Pareja, Personal, Otro)."""
    text_lower = input_text.lower()
    sens_level = compute_dynamic_sensitivity(input_text)
    risk_lvl = compute_dynamic_risk(input_text)
    rel_clean = relationship_type.strip().lower()

    # Clasificación estricta del tipo de vínculo
    if any(k in rel_clean for k in ["pareja", "enamorado", "enamorada", "novio", "novia", "esposo", "esposa"]):
        rel_category = "pareja"
    elif any(k in rel_clean for k in ["familiar", "familia", "mamá", "mama", "papá", "papa", "hermano", "hermana", "padres", "hijo", "hija"]):
        rel_category = "familiar"
    elif any(k in rel_clean for k in ["amigo", "amiga", "amistad"]):
        rel_category = "amigo"
    elif any(k in rel_clean for k in ["compañero", "trabajo", "estudio", "laboral", "jefe", "jefa", "cliente", "empresa"]):
        rel_category = "trabajo_estudio"
    elif any(k in rel_clean for k in ["conmigo", "personal", "yo", "yo mismo", "mi mismo"]):
        rel_category = "personal"
    else:
        rel_category = "otro"

    # SOBREESCRITURA DE ALTA SENSIBILIDAD: Duelo / Fallecimiento / Mascota
    if any(k in text_lower for k in ["falleció", "fallecido", "muerte", "murió", "perro", "perrito", "gato", "mascota", "luto", "duelo", "velorio", "fallecer"]):
        return AIAnalysisSchema(
            context_summary=f"Proceso de duelo y dolor por la pérdida de un ser querido o mascota en relación con ({relationship_type}). Situación: '{input_text}'.",
            detected_emotion="Tristeza Profunda y Duelo",
            emotions=[
                EmotionDetail(emotion="Tristeza", confidence=0.95),
                EmotionDetail(emotion="Dolor por Pérdida", confidence=0.88),
                EmotionDetail(emotion="Empatía", confidence=0.75)
            ],
            sensitivity_level="high",
            risk_level=risk_lvl,
            recommendation="Validar el dolor sin dar respuestas vacías; ofrecer presencia tranquila y disponibilidad sincera sin presionar por respuestas inmediatas.",
            suggested_response="Siento muchísimo lo que estás pasando. Sé cuánto significaba para ti. No hay prisa para sentirte bien; aquí estoy para cuando quieras hablar o simplemente estar acompañado.",
            alternatives=[
                AlternativeDetail(
                    title="Escucha activa y validación",
                    description="Permitir que la persona exprese sus recuerdos y dolor sin dar consejos no solicitados.",
                    benefit="Brinda un espacio seguro de desahogo y comprensión.",
                    risk="Requiere paciencia y tolerancia al silencio.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Apoyo práctico cotidiano",
                    description="Ofrecer una ayuda concreta sencilla (llevar algo de comer o acompañar en un paseo).",
                    benefit="Demuestra apoyo real sin agobiar.",
                    risk="La persona podría preferir privacidad inicial.",
                    priority=2
                )
            ]
        )

    # SOBREESCRITURA: Estrés por Exámenes / Estudios
    if any(k in text_lower for k in ["examen", "examenes", "exámenes", "estudio", "estudiar", "parcial", "finales", "universidad", "colegio", "nota", "notas"]):
        return AIAnalysisSchema(
            context_summary=f"Carga de tensión y estrés relacionada con la preparación de exámenes o entregas académicas. Situación expresada: '{input_text}'.",
            detected_emotion="Ansiedad Académica y Sobrecarga Mental",
            emotions=[
                EmotionDetail(emotion="Estrés", confidence=0.92),
                EmotionDetail(emotion="Ansiedad por Exámenes", confidence=0.85),
                EmotionDetail(emotion="Agotamiento", confidence=0.70)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="Organizar bloques cortos de estudio con la técnica Pomodoro (25 min de foco / 5 min de descanso), hidratarte y priorizar horas de sueño para fijar la memoria.",
            suggested_response="He preparado mi estudio lo mejor posible. Voy a hacer una pausa breve, respirar profundo y confiar en mi repaso sin exigirme una perfección paralizante.",
            alternatives=[
                AlternativeDetail(
                    title="Técnica Pomodoro y Pausas Activas",
                    description="Dividir la materia en bloques pequeños de 25 minutos con 5 minutos de estiramiento o descanso visual.",
                    benefit="Mantiene el enfoque y evita la fatiga mental severa.",
                    risk="Requiere alejar el teléfono durante los bloques de estudio.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Priorización de conceptos clave",
                    description="Repasar los temas principales e identificadores clave en lugar de querer releer todo el temario a última hora.",
                    benefit="Reduce la sensación de abrumamiento y fija conceptos principales.",
                    risk="Puede dejar de lado detalles secundarios poco frecuentes.",
                    priority=2
                )
            ]
        )

    # CASO 1: VÍNCULO DE PAREJA
    if rel_category == "pareja":
        return AIAnalysisSchema(
            context_summary=f"Análisis de situación afectiva con la Pareja ({relationship_type}). Situación: '{input_text}'. Objetivo: {objective}.",
            detected_emotion="Incertidumbre Afectiva y Vulnerabilidad Sentimental",
            emotions=[
                EmotionDetail(emotion="Vulnerabilidad Sentimental", confidence=0.90),
                EmotionDetail(emotion="Incertidumbre en la Relación", confidence=0.82),
                EmotionDetail(emotion="Deseo de Conexión o Cierre", confidence=0.70)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="En la relación de pareja la vulnerabilidad y la honestidad son esenciales. Expresa tus sentimientos desde lo que tú vivencias ('yo me siento...') evitando reproches defensivos o discusiones en bucle.",
            suggested_response="Valoro mucho nuestra relación y lo que compartimos. Me gustaría que conversemos con el corazón abierto y sin juzgarnos para entender cómo nos sentimos y buscar juntos la mejor forma de estar bien.",
            alternatives=[
                AlternativeDetail(
                    title="Diálogo íntimo enfocado en la comprensión mutua",
                    description="Acordar un momento a solas sin distracciones ni teléfonos para compartir sentimientos en primera persona.",
                    benefit="Profundiza la empatía, aclara malentendidos y fortalece la confianza.",
                    risk="Requiere estar emocionalmente receptivo y controlar los impulsos defensivos.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Pausa afectiva para enfriar tensiones",
                    description="Si la molestia es reciente, tomarse unas horas de calma antes de retomar la conversación.",
                    benefit="Evita decir palabras hirientes durante un pico emocional.",
                    risk="Debe aclararse expresamente el momento en que se volverá a hablar para no generar impaciencia.",
                    priority=2
                )
            ]
        )

    # CASO 2: VÍNCULO FAMILIAR
    if rel_category == "familiar":
        return AIAnalysisSchema(
            context_summary=f"Análisis de dinámica interpersonal con un Familiar ({relationship_type}). Situación: '{input_text}'. Objetivo: {objective}.",
            detected_emotion="Tensión Afectiva Familiar y Búsqueda de Armonía",
            emotions=[
                EmotionDetail(emotion="Preocupación por la Familia", confidence=0.88),
                EmotionDetail(emotion="Tensión Intergeneracional", confidence=0.79),
                EmotionDetail(emotion="Deseo de Paz y Respeto", confidence=0.68)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="La comunicación familiar requiere empatía, escucha activa y respeto mutuo. Expresa lo que sientes sin acusaciones, priorizando la paz del hogar y el resguardo del vínculo afectivo.",
            suggested_response="Hola, sé que podemos tener puntos de vista diferentes sobre esto, pero para mí la familia y nuestro bienestar siempre son lo más importante. Me gustaría que hablemos con tranquilidad para escucharnos y encontrar un punto de acuerdo.",
            alternatives=[
                AlternativeDetail(
                    title="Escucha empática y búsqueda de consensos",
                    description="Escuchar primero la perspectiva del familiar demostrando interés genuino antes de exponer tu postura.",
                    benefit="Desarma la actitud defensiva familiar y demuestra respeto filial.",
                    risk="Exige paciencia frente a posiciones tradicionales o rígidas.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Establecimiento de límites afectivos amables",
                    description="Expresar con claridad lo que necesitas o te incomoda de manera firme pero cariñosa.",
                    benefit="Previene la acumulación de resentimientos a largo plazo.",
                    risk="Puede requerir firmeza si hay resistencia inicial al cambio.",
                    priority=2
                )
            ]
        )

    # CASO 3: VÍNCULO DE AMISTAD (Amigo / Amiga)
    if rel_category == "amigo":
        return AIAnalysisSchema(
            context_summary=f"Análisis de situación interpersonal con Amigo/Amiga ({relationship_type}). Situación: '{input_text}'. Objetivo: {objective}.",
            detected_emotion="Inquietud en el Vínculo de Amistad y Lealtad",
            emotions=[
                EmotionDetail(emotion="Preocupación por la Amistad", confidence=0.87),
                EmotionDetail(emotion="Valoración de la Lealtad", confidence=0.80),
                EmotionDetail(emotion="Deseo de Claridad", confidence=0.72)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="Con tus amigos la transparencia directa y el tono sincero son el mejor camino. Habla desde el cariño y la complicidad que los une, dejando de lado el orgullo para aclarar malentendidos.",
            suggested_response="Hola, valoro muchísimo nuestra amistad y por lo mismo prefiero ser completamente transparente contigo. Me gustaría que nos tomemos algo tranquilos y hablemos sinceramente sobre lo que pasó para dejar todo claro y estar bien como siempre.",
            alternatives=[
                AlternativeDetail(
                    title="Conversación directa y sincera sin formalidades",
                    description="Plantear el tema de manera relajada y franca en persona o por llamada, evitando mensajes fríos.",
                    benefit="Aclara dudas rápidamente y refuerza la confianza de la amistad.",
                    risk="Requiere coordinar un momento libre para hablar sin prisa.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Pausa breve y reencuentro con calidez",
                    description="Permitir un par de días para enfriar cualquier molestia y reanudar el contacto con una actitud cercana.",
                    benefit="Restablece la sintonía natural sin presionar.",
                    risk="Evitar dejar pasar demasiado tiempo para que no se cree distancia.",
                    priority=2
                )
            ]
        )

    # CASO 4: VÍNCULO LABORAL / ACADÉMICO (Compañero de trabajo / estudio)
    if rel_category == "trabajo_estudio":
        return AIAnalysisSchema(
            context_summary=f"Gestión de comunicación profesional / académica con ({relationship_type}). Situación: '{input_text}'. Objetivo: {objective}.",
            detected_emotion="Inquietud Profesional e Interés en Coordinación",
            emotions=[
                EmotionDetail(emotion="Preocupación Profesional", confidence=0.89),
                EmotionDetail(emotion="Búsqueda de Claridad y Eficiencia", confidence=0.83),
                EmotionDetail(emotion="Enfoque en Objetivos", confidence=0.71)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="En el entorno de trabajo o estudio prioriza una postura objetiva, asertiva y orientada a soluciones. Separa las emociones personales de los compromisos y comunica propuestas concretas.",
            suggested_response="Hola, respecto al tema que tenemos pendiente, me gustaría que tengamos una breve reunión de 10 minutos para alinear nuestras expectativas, definir prioridades y avanzar de la forma más eficiente y respetuosa.",
            alternatives=[
                AlternativeDetail(
                    title="Propuesta estructurada de reunión o revisión",
                    description="Solicitar un breve espacio formal proponiendo 2 o 3 opciones prácticas de solución.",
                    benefit="Demuestra profesionalismo, iniciativa y optimiza el tiempo de ambos.",
                    risk="Requiere preparar los puntos clave con anticipación.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Minuta o confirmación de acuerdos por escrito",
                    description="Resumir los acuerdos o tareas acordadas tras la conversación de forma clara y amable.",
                    benefit="Garantiza respaldo y evita ambigüedades en futuras entregas.",
                    risk="Puede percibirse algo formal si el entorno de trabajo es muy casual.",
                    priority=2
                )
            ]
        )

    # CASO 5: APOYO PERSONAL / AUTOCUIDADO (Conmigo mismo)
    if rel_category == "personal":
        return AIAnalysisSchema(
            context_summary=f"Espacio de autoreflexión y autocuidado personal. Vivencia expresada: '{input_text}'.",
            detected_emotion="Abrumamiento Interior y Necesidad de Autorrespeto",
            emotions=[
                EmotionDetail(emotion="Necesidad de Calma", confidence=0.91),
                EmotionDetail(emotion="Cansancio Emocional", confidence=0.82),
                EmotionDetail(emotion="Búsqueda de Autoaceptación", confidence=0.75)
            ],
            sensitivity_level=sens_level,
            risk_level=risk_lvl,
            recommendation="Trátate con la misma compasión y paciencia que le brindarías a un buen amigo. Acepta tus límites del día de hoy y date el espacio necesario para procesar tus pensamientos sin exigencias extremas.",
            suggested_response="Reconozco lo que estoy sintiendo en este momento y elijo abordarlo con paciencia conmigo mismo/a. Respiro profundo y me doy permiso de avanzar un paso a la vez priorizando mi tranquilidad.",
            alternatives=[
                AlternativeDetail(
                    title="Pausa consciente y desahogo sin juicio",
                    description="Desconectarte de exigencias externas por 15 minutos y escribir tus pensamientos en papel para liberar la carga.",
                    benefit="Disminuye la ansiedad y aclara la mente.",
                    risk="Requiere hacer una pausa voluntaria en la rutina.",
                    priority=1
                ),
                AlternativeDetail(
                    title="Reorganización de prioridades personales",
                    description="Bajar la autoexigencia y enfocar energía solo en las actividades esenciales por el día de hoy.",
                    benefit="Protege tu salud emocional y evita el agotamiento severo.",
                    risk="Requiere posponer tareas secundarias.",
                    priority=2
                )
            ]
        )

    # CASO 6: OTRO VÍNCULO / GENERAL
    return AIAnalysisSchema(
        context_summary=f"Análisis de situación interpersonal con ({relationship_type}). Situación: '{input_text}'. Objetivo: {objective}.",
        detected_emotion="Prudencia e Incomodidad Interpersonal",
        emotions=[
            EmotionDetail(emotion="Incertidumbre", confidence=0.82),
            EmotionDetail(emotion="Preocupación", confidence=0.74),
            EmotionDetail(emotion="Deseo de Límites Sanos", confidence=0.65)
        ],
        sensitivity_level=sens_level,
        risk_level=risk_lvl,
        recommendation="Mantén una postura equilibrada, educada y asertiva. Define tus límites con amabilidad y transparencia sin involucrarte en conflictos emocionales innecesarios.",
        suggested_response="Hola, estimo que es importante mantener una comunicación transparente y respetuosa. Me gustaría que abordemos este tema con tranquilidad para llegar a un acuerdo positivo para ambos.",
        alternatives=[
            AlternativeDetail(
                title="Comunicación puntual y asertiva",
                description="Tratar únicamente el tema concreto manteniendo un trato cortés y desprovisto de confrontación.",
                benefit="Resuelve el asunto sin sobreexponerse ni generar fricciones.",
                risk="Puede sentirse distante pero preserva la paz.",
                priority=1
            ),
            AlternativeDetail(
                title="Definición de límites respetuosos",
                description="Expresar claramente tu postura con serenidad y diplomacia.",
                benefit="Protege tu tranquilidad y establece reglas claras de convivencia.",
                risk="Requiere mantener el autocontrol si la otra parte reacciona con molestia.",
                priority=2
            )
        ]
    )


def analyze_situation_with_llm(
    input_text: str,
    relationship_type: str,
    objective: str,
    communication_style: str = "empático",
    directness_level: str = "equilibrado",
    preferred_response_length: str = "medio"
) -> AIAnalysisSchema:
    """Invoca al proveedor de LLM configurado o usa el motor mock contextual si no hay API key."""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "mock" or (not settings.OPENAI_API_KEY and not settings.GEMINI_API_KEY):
        return generate_contextual_mock_analysis(input_text, relationship_type, objective)

    if provider == "openai" and settings.OPENAI_API_KEY:
        try:
            import httpx
            prompt = build_user_prompt(
                input_text, relationship_type, objective,
                communication_style, directness_level, preferred_response_length
            )
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": NEXO_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.3
                },
                timeout=15.0
            )
            if response.status_code == 200:
                raw_json = response.json()["choices"][0]["message"]["content"]
                analysis = parse_and_validate_llm_json(raw_json)
                analysis.sensitivity_level = compute_dynamic_sensitivity(input_text)
                analysis.risk_level = compute_dynamic_risk(input_text)
                return analysis
        except Exception as e:
            print(f"[LLM Exception] Fallo en llamada a OpenAI ({e}). Usando fallback contextual mock.")
            return generate_contextual_mock_analysis(input_text, relationship_type, objective)

    return generate_contextual_mock_analysis(input_text, relationship_type, objective)
