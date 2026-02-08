export interface OrchestratorOutput {
  decision: 'market_intelligence' | 'solutions_architect' | 'risk_officer' | 'executive_reviewer' | 'default';
  reasoning: string;
}

export interface AnalysisResponse {
  status?: string;
  thread_id?: string;
  orchestrator_output?: OrchestratorOutput;
  // El informe final es el resultado de la revisión ejecutiva consolidada
  final_report?: string; 
  contributions?: {
    market_intelligence?: string;
    solutions_architect?: string;
    risk_officer?: string;
    executive_reviewer?: string; 
  };
  validation?: any[];
}

export interface QueryRequest {
  user_input: string;
  thread_id: string;
}