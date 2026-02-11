import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NexusApiService } from './services/nexus-api.service';
import { AnalysisResponse } from './models/analysis.model';
import { Dossier, Consulta } from './models/dossier.model';
import { MarkdownModule } from 'ngx-markdown';
import { AgentCardComponent } from './components/agent-card/agent-card.component';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import autoTable from 'jspdf-autotable';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownModule, AgentCardComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  // --- ESTADO DE LA UI ---
  userInput: string = '';
  isProcessing: boolean = false;
  fullAnalysis: AnalysisResponse | null = null;
  isSidebarCollapsed = false;

  // --- LÓGICA DE DOSSIERS ---
  dossiers: Dossier[] = [];
  dossierSeleccionado: Dossier | null = null;
  nuevoNombreDossier: string = '';
  dossierSeleccionadoId: string | null = null;

  // El motor de la vista: historial del dossier activo
  consultasActivas: Consulta[] = [];

  // Modales
  showDeleteModal = false;
  dossierParaAccion: Dossier | null = null;

  constructor(private nexusApi: NexusApiService) { }

  ngOnInit() {
    // Usamos una clave de almacenamiento neutra para Nexus
    const saved = localStorage.getItem('NEXUS_STRATEGY_DOSSIERS');
    if (saved) {
      this.dossiers = JSON.parse(saved);
      if (this.dossiers.length > 0) {
        this.seleccionarDossier(this.dossiers[0]);
      }
    }
  }

  // --- GESTIÓN DE DOSSIERS ---
  crearDossier() {
    if (!this.nuevoNombreDossier.trim()) return;

    const nuevo: Dossier = {
      id: 'dossier-' + crypto.randomUUID(),
      nombre: this.nuevoNombreDossier.trim(),
      historial: [],
      editando: false
    };

    this.dossiers.unshift(nuevo);
    this.nuevoNombreDossier = '';
    this.guardarEnLocal();
    this.seleccionarDossier(nuevo);
  }

  seleccionarDossier(dossier: Dossier) {
    this.dossierSeleccionado = dossier;
    this.dossierSeleccionadoId = dossier.id;
    this.consultasActivas = dossier.historial || [];
    this.fullAnalysis = null;
    this.hacerScrollArriba();
  }

  confirmarEliminacion(d: Dossier, event: Event) {
    event.stopPropagation();
    this.dossierParaAccion = d;
    this.showDeleteModal = true;
  }

  eliminarDossierDefinitivo() {
    if (this.dossierParaAccion) {
      const idABorrar = this.dossierParaAccion.id;
      this.dossiers = this.dossiers.filter(d => d.id !== idABorrar);
      this.guardarEnLocal();

      if (this.dossierSeleccionado?.id === idABorrar) {
        this.dossierSeleccionado = null;
        this.dossierSeleccionadoId = null;
        this.consultasActivas = [];
      }
      this.showDeleteModal = false;
      this.dossierParaAccion = null;
    }
  }

  private guardarEnLocal() {
    localStorage.setItem('NEXUS_STRATEGY_DOSSIERS', JSON.stringify(this.dossiers));
  }

  // --- EDICIÓN DE NOMBRES ---
  activarEdicion(dossier: any, event: MouseEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.dossiers.forEach(d => d.editando = false);
    dossier.editando = true;
    dossier.nombreTemp = dossier.nombre;

    setTimeout(() => {
      const input = document.querySelector('.edit-input') as HTMLInputElement;
      if (input) {
        input.focus();
        input.select();
      }
    }, 50);
  }

  guardarNombre(dossier: any) {
    if (!dossier.editando) return;
    if (dossier.nombreTemp && dossier.nombreTemp.trim() !== "") {
      dossier.nombre = dossier.nombreTemp.trim();
      this.guardarEnLocal();
    }
    dossier.editando = false;
  }

  cancelarEdicion(dossier: any) {
    dossier.editando = false;
  }

  // --- LÓGICA DE ANÁLISIS (AGENTES) ---
  enviarConsulta() {
    if (!this.userInput.trim() || !this.dossierSeleccionado) return;

    const textoPregunta = this.userInput;
    const threadId = this.dossierSeleccionado.id;
    const fechaActual = new Date();

    // 1. PASO INSTANTÁNEO: Añadimos la pregunta del usuario al historial antes de la llamada
    // Usamos una 'decision' nula o especial para identificar que es la burbuja del usuario
    const burbujaUsuario: Consulta = {
      pregunta: textoPregunta,
      fecha: fechaActual,
      decision: null as any, // Esto hará que se renderice tu burbuja Gemini a la derecha
      respuestaHtml: '',
      razonamiento: ''
    };

    this.dossierSeleccionado.historial.push(burbujaUsuario);
    this.consultasActivas = [...this.dossierSeleccionado.historial];

    // Limpiamos UI y activamos procesamiento
    this.userInput = '';
    this.isProcessing = true;
    this.hacerScrollAbajo();

    // 2. LLAMADA AL BACKEND
    this.nexusApi.ejecutarAnalisis(textoPregunta, threadId).subscribe({
      next: (data: any) => {
        this.isProcessing = false;
        const contribuciones = data.contributions || {};

        // Mapeamos las respuestas de los agentes
        Object.keys(contribuciones).forEach(idAgente => {
          // Mantenemos tu lógica de mapeo de agentes
          const decisionClase = idAgente === 'final_report' ? 'executive_reviewer' : idAgente;

          const nuevaCardAgente: Consulta = {
            pregunta: textoPregunta,
            fecha: new Date(),
            decision: decisionClase as any,
            razonamiento: this.obtenerRazonamientoPorAgente(idAgente, data),
            respuestaHtml: contribuciones[idAgente]
          };

          this.dossierSeleccionado!.historial.push(nuevaCardAgente);
        });

        // Actualizamos la vista con todas las cards nuevas
        this.consultasActivas = [...this.dossierSeleccionado!.historial];
        this.guardarEnLocal();

        // Pequeño timeout para asegurar que el DOM se ha renderizado antes de bajar
        setTimeout(() => this.hacerScrollAbajo(), 100);
      },
      error: (err: any) => {
        console.error("Error en Nexus Engine:", err);
        this.isProcessing = false;
        // Opcional: podrías añadir una card de error aquí
      }
    });
  }

  obtenerRazonamientoPorAgente(idAgente: string, data: any): string {
    const razonamientos: { [key: string]: string } = {
      'market_intelligence': 'Investigación de mercado y análisis competitivo.',
      'solutions_architect': 'Diseño de arquitectura técnica y viabilidad.',
      'risk_officer': 'Evaluación de riesgos y cumplimiento normativo.',
      'executive_reviewer': 'Revisión ejecutiva y control de calidad final.',
      'final_report': 'Informe estratégico consolidado para gerencia.'
    };

    if (idAgente === 'final_report' && data.reasoning) {
      return data.reasoning;
    }

    return razonamientos[idAgente] || 'Análisis procesado por Nexus Engine.';
  }

  obtenerColorAgente(idAgente: string): string {
    const mapping: { [key: string]: string } = {
      'market_intelligence': 'border-market_intelligence',
      'solutions_architect': 'border-solutions_architect',
      'risk_officer': 'border-risk_officer',
      'executive_reviewer': 'border-executive_reviewer',
      'final_report': 'border-executive_reviewer' // Usamos el color de revisión para el reporte
    };

    // Si el ID no está en el mapa, devolvemos un borde por defecto
    return mapping[idAgente] || 'border-default';
  }

  // --- UTILIDADES ---
  private hacerScrollArriba() {
    setTimeout(() => {
      const container = document.querySelector('.scroll-container');
      if (container) container.scrollTo({ top: 0, behavior: 'smooth' });
    }, 50);
  }

  private hacerScrollAbajo() {
    setTimeout(() => {
      // Usamos el selector de clase que definimos en el SCSS
      const container = document.querySelector('.scroll-container');
      if (container) container.scrollTop = container.scrollHeight;
    }, 150);
  }

  async exportarDossierCompleto() {
    await this.generarPDF('content-to-export', `Dossier_${this.dossierSeleccionado?.nombre}`);
  }

  async exportarConsultaIndividual(id: string, agente: string) {
    await this.generarPDF(id, `Análisis_${agente}`);
  }

  async generarPDF(elementId: string, filename: string) {
    const element = document.getElementById(elementId);
    if (!element) return;

    this.isProcessing = true;

    try {
      const doc = new jsPDF('p', 'mm', 'a4');
      const margin = 20;
      const pageWidth = doc.internal.pageSize.getWidth();
      const maxLineWidth = pageWidth - (margin * 2);
      let cursorY = 55;

      // 1. CAPTURA DE CONTENEDOR Y TAG
      const cardContainer = element.closest('.card-analisis') || element;
      const tagElement = cardContainer.querySelector('.decision-tag');
      const agenteTexto = tagElement ? tagElement.textContent?.trim().toUpperCase() : 'NEXUS';

      // 2. PALETA DE COLORES (Tu nuevo SCSS)
      const COLORES_NEXUS = {
        MARKET: [0, 198, 255],      // #00c6ff
        SOLUTIONS: [123, 47, 247],  // #7b2ff7
        RISK: [255, 75, 43],        // #ff4b2b
        EXECUTIVE: [17, 153, 142],  // #11998e
        DEFAULT: [226, 232, 240]    // #e2e8f0
      };

      let colorRGB = COLORES_NEXUS.DEFAULT;

      // Detección por clase o por texto (seguridad extra)
      if (cardContainer.classList.contains('border-market_intelligence') || agenteTexto.includes('MARKET')) {
        colorRGB = COLORES_NEXUS.MARKET;
      } else if (cardContainer.classList.contains('border-solutions_architect') || agenteTexto.includes('SOLUTIONS')) {
        colorRGB = COLORES_NEXUS.SOLUTIONS;
      } else if (cardContainer.classList.contains('border-risk_officer') || agenteTexto.includes('RISK')) {
        colorRGB = COLORES_NEXUS.RISK;
      } else if (cardContainer.classList.contains('border-executive_reviewer') || agenteTexto.includes('EXECUTIVE')) {
        colorRGB = COLORES_NEXUS.EXECUTIVE;
      }

      const fechaHoy = new Date().toLocaleDateString('es-ES', {
        day: '2-digit', month: 'long', year: 'numeric'
      });

      // 3. CABECERA
      doc.setFillColor(colorRGB[0], colorRGB[1], colorRGB[2]);
      doc.rect(0, 0, pageWidth, 40, 'F');
      doc.setFont("helvetica", "bold");
      doc.setFontSize(22);
      doc.setTextColor(255, 255, 255);
      doc.text("NEXUS STRATEGY ENGINE", margin, 25);
      doc.setFontSize(10);
      doc.text(`INFORME: ${agenteTexto}`, margin, 32);
      doc.setFontSize(9);
      doc.setTextColor(100, 100, 100);
      doc.text(`Fecha de emisión: ${fechaHoy}`, margin, 48);

      // 4. CONTENIDO
      const contentElements = element.querySelectorAll('h1, h2, h3, h4, p, li');
      const textosVistos = new Set<string>();

      contentElements.forEach((el) => {
        let text = el.textContent?.replace(/%/g, '').replace(/\s+/g, ' ').trim() || "";
        if (text.length > 5) {
          const textLower = text.toLowerCase();
          if (!textosVistos.has(textLower)) {
            textosVistos.add(textLower);
            const isTitle = el.tagName.startsWith('H');
            doc.setFont("helvetica", isTitle ? "bold" : "normal");
            doc.setFontSize(isTitle ? 14 : 10.5);

            if (isTitle) {
              doc.setTextColor(colorRGB[0], colorRGB[1], colorRGB[2]);
            } else {
              doc.setTextColor(40, 40, 40);
            }

            const printableText = el.tagName === 'LI' ? `• ${text}` : text;
            const lines = doc.splitTextToSize(isTitle ? printableText.toUpperCase() : printableText, maxLineWidth);

            // SALTO DE PÁGINA (Llamada a this.addFooter corregida)
            if (cursorY + (lines.length * 7) > 275) {
              this.addFooter(doc, margin, agenteTexto, colorRGB);
              doc.addPage();
              cursorY = 25;
            }
            doc.text(lines, margin, cursorY);
            cursorY += (lines.length * (isTitle ? 8 : 6)) + 4;
          }
        }
      });

      // FOOTER FINAL
      this.addFooter(doc, margin, agenteTexto, colorRGB);
      doc.save(`${filename}.pdf`);

    } catch (err) {
      console.error("Error:", err);
    } finally {
      this.isProcessing = false;
    }
  }

  private addFooter(doc: any, margin: number, agente: string, color: number[]) {
    const pageCount = doc.internal.getNumberOfPages();
    const pageHeight = doc.internal.pageSize.getHeight();
    const pageWidth = doc.internal.pageSize.getWidth();

    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setDrawColor(color[0], color[1], color[2]);
      doc.setLineWidth(0.5);
      doc.line(margin, pageHeight - 15, pageWidth - margin, pageHeight - 15);
      doc.setFontSize(8);
      doc.setTextColor(150, 150, 150);
      doc.text(`Generado por Inteligencia Nexus (${agente}) - Página ${i} de ${pageCount}`, margin, pageHeight - 10);
    }
  }
}

