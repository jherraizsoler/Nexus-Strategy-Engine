import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common'; // Importante para el pipe de fecha

@Component({
  selector: 'app-orchestrator-logs',
  standalone: true,
  imports: [CommonModule], // Asegúrate de que CommonModule esté aquí
  templateUrl: './orchestrator-logs.html',
  styleUrl: './orchestrator-logs.scss',
})
export class OrchestratorLogs {
  @Input() logs: string[] = [];
  @Input() status: string = 'Inactivo';

  // Define la variable que falta
  now: Date = new Date();

  constructor() {
    // Opcional: Actualizar la hora cada segundo para que los logs sean precisos
    setInterval(() => {
      this.now = new Date();
    }, 1000);
  }
}