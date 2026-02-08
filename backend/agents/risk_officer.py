from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.state.schema import AgentState

# Configuración del modelo (temperatura 0 para asegurar objetividad y rigor en el análisis de riesgos)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def risk_officer_agent(state: AgentState):
    """
    Agente de Gestión de Riesgos y Cumplimiento Normativo.
    Audita las propuestas estratégicas y técnicas para mitigar vulnerabilidades
    operativas, legales y de seguridad.
    """
    
    # Recopilación del contexto multidisciplinar generado por el Engine
    market_info = state["contributions"].get("market_intelligence", "No se ha proporcionado análisis de mercado.")
    tech_info = state["contributions"].get("solutions_architect", "No se ha proporcionado arquitectura técnica.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres el Chief Risk Officer (CRO) del Nexus Strategy Engine. 
        Tu responsabilidad es actuar como el último filtro de seguridad y viabilidad antes de la revisión ejecutiva.
        
        VECTORES DE AUDITORÍA:
        1. Marco Normativo y Cumplimiento: Evalúa la alineación con GDPR, marcos regulatorios locales y estándares del sector.
        2. Riesgos Operativos y de Ejecución: Identifica dependencias críticas, infraestructuras frágiles o costes ocultos.
        3. Seguridad y Ética de IA: Audita la privacidad de los datos, el riesgo de sesgos y la integridad en el uso de LLMs.

        ENTRADA DE CONTEXTO:
        - Análisis de Estrategia: {market_context}
        - Especificaciones Técnicas: {tech_context}

        INSTRUCCIONES:
        Tu análisis debe ser crítico, incisivo y directo. Tu objetivo no es aprobar, sino anticipar fallos operativos 
        y legales que pongan en compromiso la integridad del proyecto."""),
        ("human", "{messages}")
    ])

    # Ejecución de la auditoría de riesgos
    chain = prompt | llm
    response = chain.invoke({
        "messages": state["messages"],
        "market_context": market_info,
        "tech_context": tech_info
    })

    # Gestión de estado: Actualización del repositorio de contribuciones
    current_contributions = dict(state.get("contributions", {}))
    current_contributions["risk_officer"] = response.content

    return {
        "messages": [response],
        "contributions": current_contributions,
        "next_step": "orchestrator"  # Retorno al nodo de decisión central para validación
    }