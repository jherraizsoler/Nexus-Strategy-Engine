import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AnalysisResponse, QueryRequest } from '../models/analysis.model';

@Injectable({
  providedIn: 'root',
})
export class NexusApiService {
  private apiUrl = 'http://localhost:8000';

  // ID del hilo de ejecución para la persistencia en el motor
  private currentThreadId: string = 'nexus-default-session';

  constructor(private http: HttpClient) { }

  /**
   * Vincula la sesión actual a un Dossier específico.
   */
  setThreadId(id: string) {
    this.currentThreadId = id;
    console.log(`[Nexus Engine] Memoria vinculada al Dossier: ${id}`);
  }

  /**
   * Envía la consulta a la arquitectura multi-agente del Nexus Strategy Engine.
   * El orquestador derivará la tarea a los especialistas correspondientes.
   */
  ejecutarAnalisis(pregunta: string, threadId: string): Observable<any> {
    const body: QueryRequest = {
      user_input: pregunta,
      thread_id: threadId || this.currentThreadId
    };
    
    return this.http.post<any>(`${this.apiUrl}/analyze`, body);
  }
}