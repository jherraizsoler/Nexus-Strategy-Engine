from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.state.schema import AgentState

# Configuración del motor técnico (Temperatura 0.1 para priorizar precisión y rigor arquitectónico)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

def solutions_architect_agent(state: AgentState):
    """
    Agente de Arquitectura de Soluciones y Estrategia Tecnológica.
    Diseña ecosistemas de software escalables y selecciona el stack tecnológico
    alineado con los objetivos de negocio previamente definidos.
    """
    
    # Sincronización con el análisis estratégico previo (Nexus Core Data)
    market_analysis = state["contributions"].get("market_intelligence", "Contexto estratégico no disponible")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres el Chief Technology Officer (CTO) del Nexus Strategy Engine. 
        Tu objetivo es traducir los requisitos de negocio en una arquitectura técnica de vanguardia.

        DIMENSIONES TÉCNICAS A DEFINIR:
        1. Stack Tecnológico: Selecciona y justifica el ecosistema ideal (ej. .NET 8, Python/FastAPI, Cloud Native, etc.).
        2. Viabilidad y Trade-offs: Analiza críticamente pros y contras de las tecnologías propuestas.
        3. Diseño de Infraestructura: Define patrones de integración, escalabilidad, microservicios y orquestación de IA.
        4. Alineación Estratégica: Justifica por qué esta arquitectura es el motor óptimo para alcanzar los objetivos de mercado.

        REGLA OPERATIVA: Mantente estrictamente en el dominio técnico y de infraestructura. 
        El análisis de riesgos legales y cumplimiento normativo será gestionado por el Risk Officer.
        
        CONTEXTO ESTRATÉGICO DE ENTRADA: {market_context}"""),
        ("human", "{messages}")
    ])

    # Ejecución del diseño arquitectónico
    chain = prompt | llm
    response = chain.invoke({
        "messages": state["messages"],
        "market_context": market_analysis
    })

    # Actualización del estado global de contribuciones del proyecto
    current_contributions = state.get("contributions", {})

    return {
        "messages": [response],
        "contributions": {**current_contributions, "solutions_architect": response.content}
    }