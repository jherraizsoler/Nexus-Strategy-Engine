import json
import traceback
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.state.schema import AgentState

# Motor de decisión (Temperatura 0 para garantizar consistencia lógica absoluta)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def strategic_orchestrator(state: AgentState):
    """
    Cerebro del Nexus Strategy Engine. 
    Analiza el estado actual del proyecto, evalúa las contribuciones de los expertos
    y determina la siguiente fase del flujo estratégico.
    """
    
    # Análisis de la cobertura actual del informe
    current_contributions = state.get("contributions", {})
    expertos_que_han_participado = list(current_contributions.keys())

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres el Chief Strategy Orchestrator del Nexus Strategy Engine. 
        Tu misión es coordinar una respuesta multidisciplinar de alto impacto para el usuario.
        
        PANEL DE EXPERTOS DISPONIBLES:
        - 'market_intelligence': Especialista en análisis de mercado, competencia y propuesta de valor.
        - 'solutions_architect': Especialista en diseño técnico, stack tecnológico y escalabilidad.
        - 'risk_officer': Auditor de riesgos operativos, legales y de seguridad.
        - 'executive_reviewer': Auditor final OBLIGATORIO para consolidación y Scoring.

        PROTOCOLOS DE DECISIÓN:
        1. Evaluación: Analiza si con las aportaciones actuales ({contributions}) se ha cubierto la demanda del usuario.
        2. Selección: Si falta profundidad estratégica o técnica, activa al experto correspondiente.
        3. Priorización: Si los expertos ya han aportado su valor, deriva a 'executive_reviewer'.
        4. Cierre: Solo si el 'executive_reviewer' ha certificado el informe, responde 'FINISH'.

        Tu respuesta debe ser estrictamente un JSON válido:
        {{
            "next_step": "nombre_del_experto_o_FINISH", 
            "reasoning": "Justificación técnica de la secuencia elegida basándote en el estado actual."
        }}"""),
        ("human", "{messages}")
    ])

    chain = prompt | llm
    
    # Invocación del modelo de decisión
    response = chain.invoke({
        "messages": state["messages"],
        "contributions": expertos_que_han_participado
    })

    try:
        # Extracción y limpieza segura del JSON (robusteza ante posibles prefijos del modelo)
        raw_content = response.content.strip()
        start_idx = raw_content.find('{')
        end_idx = raw_content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            raw_content = raw_content[start_idx:end_idx + 1]

        decision = json.loads(raw_content)
        next_agent = decision.get("next_step", "executive_reviewer")
        reasoning = decision.get("reasoning", "Continuando con el flujo de auditoría estándar.")
        
        print(f"\n[NEXUS ORCHESTRATOR]: Siguiente fase -> {next_agent}")
        print(f"[RAZONAMIENTO]: {reasoning}\n")
        
        return {"next_step": next_agent}
    
    except Exception as e:
        print(f"⚠️ Error en el parsing de decisión: {e}")
        # Protocolo de seguridad: Forzar revisión ejecutiva para evitar bucles infinitos
        return {"next_step": "executive_reviewer"}