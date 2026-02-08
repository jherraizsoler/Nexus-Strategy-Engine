import os
import traceback
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Infraestructura de Grafo de Estados (Nexus Core)
from langgraph.graph import StateGraph, START, END
from backend.state.schema import AgentState
from backend.state.checkpointer import get_checkpointer  # Ajustado a la ruta que definimos

# Importación de Agentes Especialistas (Nexus Strategy Engine)
from backend.agents.orchestrator import strategic_orchestrator
from backend.agents.market_intelligence import market_intelligence_agent
from backend.agents.solutions_architect import solutions_architect_agent
from backend.agents.risk_officer import risk_officer_agent
from backend.agents.executive_reviewer import executive_reviewer_agent

load_dotenv()

# --- CONFIGURACIÓN DEL ENGINE (GRAFO) ---

builder = StateGraph(AgentState)

# Definición de Nodos de Inteligencia
builder.add_node("orchestrator", strategic_orchestrator)
builder.add_node("market_intelligence", market_intelligence_agent)
builder.add_node("solutions_architect", solutions_architect_agent)
builder.add_node("risk_officer", risk_officer_agent)
builder.add_node("executive_reviewer", executive_reviewer_agent)

# Estructura de Flujo Base
builder.add_edge(START, "orchestrator")
builder.add_edge("market_intelligence", "orchestrator")
builder.add_edge("solutions_architect", "orchestrator")
builder.add_edge("risk_officer", "orchestrator")
# El revisor es el único que puede llevar al fin del proceso
builder.add_edge("executive_reviewer", END)

def route_next(state: AgentState):
    """
    Lógica de enrutamiento dinámico para el Nexus Strategy Engine.
    Gestiona la transición entre expertos y evita bucles operativos.
    """
    next_node = state.get("next_step")
    contributions = state.get("contributions", {})

    # Salvaguarda de integridad: Evita re-procesamiento innecesario si el agente ya aportó
    if next_node in contributions and next_node != "executive_reviewer":
        return "executive_reviewer"

    # Verificación de consenso final: Si el orquestador dice terminar o no hay paso claro
    if next_node == "FINISH" or not next_node:
        if "executive_reviewer" not in contributions:
            return "executive_reviewer"
        return END
    
    return next_node

# Configuración de aristas condicionales (Orquestación dinámica de Nexus)
builder.add_conditional_edges(
    "orchestrator", 
    route_next,
    {
        "market_intelligence": "market_intelligence",
        "solutions_architect": "solutions_architect",
        "risk_officer": "risk_officer",
        "executive_reviewer": "executive_reviewer",
        "FINISH": END
    }
)

# Compilación del grafo con persistencia de hilos (Nexus Persistence)
memory = get_checkpointer()
graph = builder.compile(checkpointer=memory)

# --- SERVIDOR API (FASTAPI) ---

app = FastAPI(
    title="Nexus Strategy Engine",
    description="Engine de orquestación multi-agente para análisis estratégico de alto impacto.",
    version="1.0.0"
)

# Configuración de CORS para el Front de Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", # Tu Front de Angular local
        "http://127.0.0.1:4200"  # Alternativa común de loopback
    ],
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, DELETE, etc.
    allow_headers=["*"], # Permite enviar tokens y tipos de contenido
)

class QueryRequest(BaseModel):
    user_input: str
    thread_id: str = "nexus_default_session"

@app.post("/analyze")
async def run_analysis(request: QueryRequest):
    """
    Endpoint principal para la ejecución de flujos estratégicos de Nexus.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # Inicialización del estado conforme a la identidad Nexus
    initial_input = {
        "messages": [("user", request.user_input)],
        "contributions": {},
        "validation_results": [],
        "next_step": ""
    }
    
    try:
        final_state = graph.invoke(initial_input, config)
        return {
            "status": "success",
            "thread_id": request.thread_id,
            "contributions": final_state.get("contributions", {}),
            "validation": final_state.get("validation_results", [])
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en el Nexus Engine: {str(e)}")

@app.get("/health")
def health_check():
    """Estado de salud del sistema Nexus."""
    return {
        "status": "online", 
        "engine": "Nexus Strategy Engine",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)