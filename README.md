# Nexus Strategy Engine (NSE) - Multi-Agent AI System 🚀

**Nexus Strategy Engine** es una plataforma avanzada de análisis estratégico que utiliza una arquitectura de **grafos de agentes inteligentes** para procesar, auditar y sintetizar información compleja para la toma de decisiones directivas.

El sistema integra una interfaz profesional reactiva en **Angular 18** con un motor de orquestación de agentes basado en **LangGraph (Python/FastAPI)**.

---

## 📌 Índice General

1. [🏛️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
2. [📂 Estructura del Repositorio y Documentación](#-estructura-del-repositorio)
3. [🤖 Flujo de Trabajo de los Agentes](#-flujo-de-trabajo-de-los-agentes)
4. [⚖️ Trade-offs Técnicos](#️-trade-offs-técnicos-y-decisiones-de-diseño)
5. [🚀 Guía de Instalación Rápida](#-guía-de-instalación-rápida)
6. [🛠️ Stack Tecnológico](#️-stack-tecnológico)

---

## 🏛️ Arquitectura del Sistema
El sistema se divide en dos componentes principales diseñados para trabajar de forma coordinada bajo principios de escalabilidad y observabilidad:

* **Frontend (Dashboard):** Interfaz profesional que permite la entrada de datos, gestión de hilos de conversación y visualización de resultados mediante Markdown jerárquico.
* **Backend (Core de IA):** Motor de razonamiento que utiliza una topología de grafo para que agentes especializados colaboren bajo supervisión técnica.

#### 📊 Diagrama Arquitectura
![Arquitectura del Sistema](./assets/diagrama_arquitectura.png)

> **Nota:** Se utiliza una topología de grafo donde el **Orchestrator** gestiona el flujo entre especialistas, apoyado en un checkpointer de SQLite para la persistencia de hilos de conversación.
---

## 📂 Estructura del Repositorio

Para información técnica detallada de cada módulo, consulte sus respectivos manuales:

### 🔹 [Backend - Core de IA e Infraestructura](./backend/README.md)
* **Contenidos destacados:**
    * Configuración del entorno Python (VENV).
    * Definición de Agentes (**Orchestrator, Market Intelligence, Solutions Architect, Risk Officer, Executive Reviewer**).
    * Lógica del Grafo de Estados (**LangGraph**).
    * Persistencia de memoria con **SQLite Checkpointer**.
    * Documentación de la API (**FastAPI + Swagger**).

### 🔸 [Frontend - Interfaz de Usuario Avanzada](./frontend/README.md)
* **Contenidos destacados:**
    * Requisitos de Node.js y Angular CLI.
    * Integración de `ngx-markdown` para reportes.
    * Servicios de comunicación (**HttpClient** y **RxJS**).
    * Configuración de Estilos **SCSS** (UI/UX Premium).

---

## 🤖 Flujo de Trabajo de los Agentes

El Hub de Agentes de **Nexus Strategy Engine** opera bajo una jerarquía de especialización para garantizar el rigor técnico del output:

1.  **Strategic Orchestrator:** Gestiona el estado de la consulta y delega tareas según la fase del análisis.
2.  **Market Intelligence Agent:** Procesa el contexto de negocio, objetivos estratégicos y entorno competitivo.
3.  **Solutions Architect Agent:** Diseña la propuesta técnica y arquitectura de sistemas (especializado en .NET 8).
4.  **Risk Officer Agent:** Evalúa riesgos normativos, legales (GDPR) y de seguridad de datos.
5.  **Executive Reviewer:** Realiza el control de calidad final, asegura la coherencia y asigna un Score de Validación.



---

## ⚖️ Trade-offs Técnicos y Decisiones de Diseño

Dada la naturaleza de la prueba y el límite de tiempo de **6 días**, se tomaron decisiones estratégicas priorizando la **arquitectura y la extensibilidad** sobre la completitud absoluta:

* **LangGraph vs. Cadenas Lineales:** Se optó por una arquitectura de grafos para permitir **ciclos de retroalimentación** (*feedback loops*) entre el `Executive Reviewer` y los agentes especialistas, garantizando una calidad técnica superior al permitir revisiones dinámicas.
* **Persistencia en SQLite:** Se eligió SQLite como `checkpointer` por su nula fricción de instalación para el evaluador, permitiendo gestionar memoria de hilos de conversación sin requerir infraestructuras externas complejas en esta fase.
* **Aislamiento de Entornos (Docker):** Se priorizó la contenedorización mediante `docker-compose` para garantizar que el sistema funcione de forma idéntica en cualquier máquina, eliminando riesgos por versiones de Node.js o Python locales.
* **Mocking de Herramientas de Búsqueda:** Para asegurar la estabilidad de la demo, los agentes utilizan una base de conocimiento interna optimizada. Esto evita fallos por cuotas de API externas o latencias de red durante la revisión.
* **Arquitectura Angular Standalone:** Se utilizó **Angular 18** con componentes *standalone* para reducir el *boilerplate* y mejorar la velocidad de carga, enfocando el esfuerzo en la visualización de las trazas de decisión de los agentes.

---

## 🚀 Guía de Instalación Rápida

1.  **Configuración:** Cree un archivo `.env` dentro de la carpeta `backend/` y añada su clave de OpenAI:
    ```env
    OPENAI_API_KEY="tu_clave_aquí"
    ```
2.  **Despliegue con Docker:** Desde la raíz del proyecto, ejecute:
    ```bash
    docker-compose up --build
    ```
3.  **Acceso al Sistema:**
    * **Interfaz de Usuario:** `http://localhost:4200`
    * **Documentación de API:** `http://localhost:8000/docs`

---


## 🛠️ Stack Tecnológico

* **Frontend:** Angular 18, TypeScript, SCSS, RxJS.
* **Backend:** Python 3.11+, FastAPI, LangGraph, LangChain.
* **IA:** Modelos GPT-4o .
* **Persistencia:** SQLite (Estados) y ChromaDB (Memoria Vectorial).

---

---
## 📄 Licencia
Este proyecto se distribuye bajo la licencia **CC BY-NC-ND 4.0**. Se permite su visualización y descarga con fines exclusivamente académicos y de evaluación técnica. Queda prohibida cualquier explotación comercial o distribución de versiones derivadas.

---
**Desarrollado por Jorge Herráiz.**
