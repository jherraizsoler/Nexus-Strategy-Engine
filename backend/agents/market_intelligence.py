from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.state.schema import AgentState

# Configuración del motor de inteligencia (Temperatura 0.3 para permitir un análisis creativo pero controlado)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def market_intelligence_agent(state: AgentState):
    """
    Agente de Inteligencia de Mercado y Estrategia.
    Analiza el ecosistema competitivo, identifica oportunidades de mercado 
    y define los pilares estratégicos de la propuesta.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres el Senior Strategy Consultant del Nexus Strategy Engine. 
        Tu misión es procesar la solicitud ejecutiva y generar un análisis de mercado de alta precisión.
        
        DIMENSIONES DE ANÁLISIS:
        1. Objetivos Estratégicos: Identifica las metas críticas y los KPIs implícitos.
        2. Ecosistema Competitivo: Analiza las fuerzas del mercado y las tendencias del sector específico.
        3. Arquitectura de Valor: Define la propuesta diferenciadora y las ventajas competitivas.

        REQUISITOS DE SALIDA:
        - Tono: Ejecutivo, directo y orientado a resultados.
        - Formato: Estructura profesional apta para comités de dirección.
        - Objetivo: Tu análisis servirá de base para la arquitectura técnica y la evaluación de riesgos."""),
        ("human", "{messages}")
    ])

    # Ejecución de la cadena de análisis estratégico
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})

    # Actualización del repositorio de contribuciones del Nexus Engine
    contributions = state.get("contributions", {})
    contributions["market_intelligence"] = response.content

    return {
        "messages": [response],
        "contributions": contributions
    }