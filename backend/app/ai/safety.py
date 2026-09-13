import re
from typing import Optional
from pydantic import BaseModel


class SafetyResult(BaseModel):
    is_safe: bool
    risk_level: str  # low, medium, high, critical
    category: str    # general, autolesion, violencia, abuso, emergencia
    action_taken: str
    safety_message: Optional[str] = None


# Patrones de palabras clave e intenciones sensibles
RISK_PATTERNS = {
    "autolesion": [
        r"\b(suicid|matarm|cortarm|quitarme la vida|no quiero vivir|acabar con todo|hacerme daño|desaparecer para siempre)\b"
    ],
    "violencia": [
        r"\b(golpear|matar a|hacer daño a|navaja|arma|violencia física|amenazar de muerte|atacar a)\b"
    ],
    "abuso": [
        r"\b(abuso sexual|violación|agresión sexual|acoso constante|maltrato físico)\b"
    ],
    "emergencia": [
        r"\b(sobredosis|inconsciente|sangrando mucho|convulsiones|emergencia médica)\b"
    ]
}

SAFETY_WARNING_TEMPLATE = (
    "⚠️ Esta situación puede requerir ayuda inmediata o intervención profesional. "
    "NEXO es una herramienta de apoyo reflexivo y no reemplaza la atención de un profesional ni los servicios de emergencia.\n\n"
    "Si tú o alguien conocido está atravesando un momento de crisis, autolesión o violencia, por favor contacta a la línea de ayuda o emergencia de tu localidad de forma inmediata."
)


def evaluate_safety(input_text: str) -> SafetyResult:
    """Analiza el texto ingresado para clasificar el nivel de riesgo antes de llamar al LLM."""
    text_lower = input_text.lower()

    for category, patterns in RISK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return SafetyResult(
                    is_safe=False,
                    risk_level="critical" if category in ["autolesion", "violencia"] else "high",
                    category=category,
                    action_taken="Intercepción de seguridad pre-LLM ejecutada. Respuesta humana de auxilio enviada.",
                    safety_message=SAFETY_WARNING_TEMPLATE
                )

    return SafetyResult(
        is_safe=True,
        risk_level="low",
        category="general",
        action_taken="Análisis de seguridad superado sin alertas.",
        safety_message=None
    )
