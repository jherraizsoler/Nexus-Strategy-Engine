import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';

@Component({
  selector: 'app-agent-card',
  standalone: true,
  imports: [CommonModule, MarkdownModule],
  templateUrl: './agent-card.component.html',
  styleUrl: './agent-card.component.scss'
})
export class AgentCardComponent {
  @Input() agentName: string = ''; // ID del nodo: market_intelligence, etc.
  @Input() content: string = '';
  @Input() role: string = '';      // Nombre legible: 'Analista de Mercado'

  /**
   * Asigna el esquema de colores de Nexus según el rol técnico del agente.
   */
  getAgentTheme() {
    const themes: { [key: string]: string } = {
      'market_intelligence': 'border-market_intelligence', 
      'solutions_architect': 'border-solutions_architect',
      'risk_officer':        'border-risk_officer',
      'executive_reviewer':  'border-executive_reviewer',
      'final_report':        'border-executive_reviewer'
    };
    return themes[this.agentName] || 'border-default';
  }

  // Traducción de iconos por rol
  getAgentIcon() {
    const icons: { [key: string]: string } = {
      'market_intelligence': 'chart-line',
      'solutions_architect': 'terminal',
      'risk_officer': 'shield-check',
      'executive_reviewer': 'gavel'
    };
    return icons[this.agentName] || 'robot';
  }
}