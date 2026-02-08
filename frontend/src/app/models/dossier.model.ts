// src/app/models/dossier.model.ts
export interface Consulta {
  pregunta: string;
  fecha: Date;
  decision: 'market_intelligence' | 'solutions_architect' | 'risk_officer' | 'executive_reviewer' | 'final_report' | 'default';
  razonamiento: string;
  respuestaHtml: string;
}

export interface Dossier {
  id: string;
  nombre: string;
  historial: Consulta[]; // Importante: lo ideal es que esto venga vacío al principio
  editando?: boolean;
  nombreTemp?: string;
}