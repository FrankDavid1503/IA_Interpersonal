import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.situation import Situation
from app.models.analysis import Analysis
from app.models.emotion import AnalysisEmotion
from app.models.recommendation import Recommendation
from app.models.preference import UserPreference
from app.services.safety_service import check_and_record_safety
from app.ai.agent import analyze_situation_with_llm
from app.schemas.analysis import AnalysisResponse, EmotionResponse, RecommendationResponse


def run_analysis_for_situation(db: Session, user_id: uuid.UUID, situation_id: uuid.UUID) -> AnalysisResponse:
    """Ejecuta el pipeline completo de análisis: Safety Check -> LLM -> Persistencia en BD."""
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Situación no encontrada.")
    if situation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos sobre esta situación.")

    # 1. Capa de Seguridad (Pre-LLM)
    safety_result = check_and_record_safety(db, situation_id, situation.input_text)
    if not safety_result.is_safe:
        # En caso de riesgo elevado, se retorna respuesta de seguridad predeterminada sin llamar al LLM
        mock_analysis = Analysis(
            situation_id=situation.id,
            context_summary="Situación interceptada por protocolo de seguridad y evaluación de riesgo.",
            detected_emotion="Alerta / Crisis",
            sensitivity_level="high",
            risk_level=safety_result.risk_level,
            recommendation="Se requiere intervención o ayuda humana profesional.",
            suggested_response=safety_result.safety_message or "Por favor busca asistencia especializada.",
            model_name="safety-interceptor"
        )
        db.add(mock_analysis)
        db.commit()
        db.refresh(mock_analysis)
        
        return AnalysisResponse(
            id=mock_analysis.id,
            situation_id=situation.id,
            context_summary=mock_analysis.context_summary,
            detected_emotion=mock_analysis.detected_emotion,
            sensitivity_level=mock_analysis.sensitivity_level,
            risk_level=mock_analysis.risk_level,
            recommendation=mock_analysis.recommendation,
            suggested_response=mock_analysis.suggested_response,
            model_name=mock_analysis.model_name,
            created_at=mock_analysis.created_at,
            emotions=[],
            recommendations=[],
            safety_warning=safety_result.safety_message
        )

    # 2. Consultar Preferencias de Usuario
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    comm_style = pref.communication_style if pref else "empático"
    directness = pref.directness_level if pref else "equilibrado"
    pref_len = pref.preferred_response_length if pref else "medio"

    # 3. Invocar al Agente de IA
    ai_output = analyze_situation_with_llm(
        input_text=situation.input_text,
        relationship_type=situation.relationship_type,
        objective=situation.objective,
        communication_style=comm_style,
        directness_level=directness,
        preferred_response_length=pref_len
    )

    # 4. Guardar Análisis Principal
    db_analysis = Analysis(
        situation_id=situation.id,
        context_summary=ai_output.context_summary,
        detected_emotion=ai_output.detected_emotion,
        sensitivity_level=ai_output.sensitivity_level,
        risk_level=ai_output.risk_level,
        recommendation=ai_output.recommendation,
        suggested_response=ai_output.suggested_response,
        model_name=f"nexo-agent-{settings_llm_name()}"
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    # 5. Guardar Emociones Secundarias y Alternativas
    emotions_db = []
    for em in ai_output.emotions:
        db_em = AnalysisEmotion(
            analysis_id=db_analysis.id,
            emotion=em.emotion,
            confidence=em.confidence
        )
        db.add(db_em)
        emotions_db.append(db_em)

    recs_db = []
    for alt in ai_output.alternatives:
        db_rec = Recommendation(
            analysis_id=db_analysis.id,
            title=alt.title,
            description=alt.description,
            benefit=alt.benefit,
            risk=alt.risk,
            priority=alt.priority
        )
        db.add(db_rec)
        recs_db.append(db_rec)

    db.commit()
    db.refresh(db_analysis)

    return AnalysisResponse(
        id=db_analysis.id,
        situation_id=situation.id,
        context_summary=db_analysis.context_summary,
        detected_emotion=db_analysis.detected_emotion,
        sensitivity_level=db_analysis.sensitivity_level,
        risk_level=db_analysis.risk_level,
        recommendation=db_analysis.recommendation,
        suggested_response=db_analysis.suggested_response,
        model_name=db_analysis.model_name,
        created_at=db_analysis.created_at,
        emotions=[EmotionResponse.model_validate(e) for e in emotions_db],
        recommendations=[RecommendationResponse.model_validate(r) for r in recs_db],
        safety_warning=None
    )


def get_analysis_by_id(db: Session, user_id: uuid.UUID, analysis_id: uuid.UUID) -> AnalysisResponse:
    """Consulta el detalle de un análisis por ID de análisis o ID de situación con verificación de permisos."""
    # 1. Intentar buscar por ID de análisis directo
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

    # 2. Si no existe como ID de análisis, buscar si es un ID de situación
    if not analysis:
        situation = db.query(Situation).filter(Situation.id == analysis_id, Situation.user_id == user_id).first()
        if situation:
            analysis = db.query(Analysis).filter(Analysis.situation_id == situation.id).order_by(Analysis.created_at.desc()).first()
            # Si la situación no tenía análisis en BD, ejecutarlo inmediatamente
            if not analysis:
                return run_analysis_for_situation(db=db, user_id=user_id, situation_id=situation.id)

    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Análisis no encontrado.")

    situation = db.query(Situation).filter(Situation.id == analysis.situation_id).first()
    if not situation or situation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes autorización para ver este análisis.")

    return AnalysisResponse.model_validate(analysis)


def settings_llm_name() -> str:
    from app.core.config import settings
    return settings.LLM_PROVIDER

