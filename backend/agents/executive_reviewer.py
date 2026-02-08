from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.state.schema import AgentState

# Configuración del motor de razonamiento (Temperatura 0 para máxima consistencia en auditoría)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def executive_reviewer_agent(state: AgentState):
    """
    Agente de Auditoría Estratégica y Consolidación.
    Analiza las aportaciones de los especialistas, asigna métricas de calidad (Quality Score)
    y genera el entregable final estructurado.
    """
    
    # Recuperamos las contribuciones acumuladas en el estado del motor
    contributions = state.get("contributions", {})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres el Lead Executive Reviewer del Nexus Strategy Engine. 
        Tu función es realizar el control de calidad integral y la síntesis del informe estratégico.
        
        DIRECTRICES DE AUDITORÍA:
        1. Evaluar la alineación entre los objetivos de mercado, la arquitectura técnica y los riesgos identificados.
        2. Asignar un 'Quality Score' (escala 0-10) proporcionando una justificación ejecutiva de la métrica.
        3. Consolidar el informe final utilizando un formato Markdown jerárquico de alto nivel.

        MÓDULOS A AUDITAR:
        - Inteligencia de Mercado: {market}
        - Arquitectura de Soluciones: {tech}
        - Gestión de Riesgos: {risk}

        Tu respuesta debe ser el informe final consolidado, finalizando con una sección de 
        'Certificación Ejecutiva' que incluya el Score de Calidad."""),
        ("human", "{messages}")
    ])

    # Ejecución de la cadena de consolidación
    chain = prompt | llm
    response = chain.invoke({
        "messages": state["messages"],
        "market": contributions.get("market_intelligence", "Información no disponible"),
        "tech": contributions.get("solutions_architect", "Información no disponible"),
        "risk": contributions.get("risk_officer", "Información no disponible")
    })

    # Registro de métricas de validación para el seguimiento del flujo
    validation = {
        "agent": "executive_reviewer",
        "status": "finalized",
        "audit_complete": True,
        "quality_score_generated": True
    }

    return {
        "messages": [response],
        "validation_results": [validation],
        # Integramos el informe final en el repositorio de contribuciones
        "contributions": {**contributions, "final_report": response.content},
        "next_step": "FINISH"
    }