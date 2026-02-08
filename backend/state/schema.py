from typing import Annotated, TypedDict, Dict, List, Any
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Define el esquema de estado global para el Nexus Strategy Engine.
    Mantiene la trazabilidad de las contribuciones y el historial de ejecución.
    """
    
    # Historial de interacciones gestionado automáticamente por el motor de grafo
    messages: Annotated[list, add_messages]
    
    # Registro de aportaciones específicas de cada agente especialista
    contributions: Dict[str, str]
    
    # Resultados de auditoría y métricas de calidad (Scoring) generados por los revisores
    validation_results: List[Dict[str, Any]]
    
    # Indicador de flujo para el enrutamiento dinámico del orquestador
    next_step: str