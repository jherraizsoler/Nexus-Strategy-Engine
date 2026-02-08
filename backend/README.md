# Nexus Strategy Engine (NSE) - Multi-Agent AI System 🚀

**Nexus Strategy Engine** es un sistema multi-agente de alto nivel diseñado para transformar consultas estratégicas en informes de viabilidad estructurados. El sistema utiliza una arquitectura de orquestación explícita mediante grafos de estado para coordinar especialistas en análisis de mercado, arquitectura técnica y auditoría de riesgos.

---

## 📖 Índice de Contenidos (Backend)

* ⬅️ **[Volver al README Principal](../README.md)**

1. [🏗️ Arquitectura y Decisiones Técnicas](#️-arquitectura-y-decisiones-técnicas)
    * [1. Orquestación Dinámica (Supervisor Pattern)](#1-orquestación-dinámica-supervisor-pattern)
    * [2. Roles Profesionales Especializados](#2-roles-profesionales-especializados)
    * [3. Persistencia de Estado mediante Checkpointers](#3-persistencia-de-estado-mediante-checkpointers)
2. [🛠️ Stack Tecnológico](#️-stack-tecnológico)
3. [🚀 Instalación y Ejecución](#-instalación-y-ejecución)
    * [1. Clonar el repositorio](#1-clonar-el-repositorio)
    * [2. Configuración de Variables de Entorno](#2-configuración-de-variables-de-entorno)
    * [3. Ejecución con Docker (Recomendado)](#3-ejecución-con-docker-recomendado)
    * [4. Ejecución Local (Backend)](#4-ejecución-local-backend)
4. [⚠️ Ajuste de Rutas e Importaciones](#️-ajuste-de-rutas-e-importaciones-importante)
5. [🌐 Acceso al Sistema](#-acceso-al-sistema)
6. [🚀 Ejemplos de Uso y Validación Técnica](#-ejemplos-de-uso-y-validación-técnica)
    * [🔄 Prueba de Persistencia (Seguimiento)](#-prueba-de-persistencia-seguimiento)
7. [📈 Interpretación de Resultados (Logs del Servidor)](#-interpretación-de-resultados-logs-del-servidor)
8. [📊 Observabilidad y Trazabilidad](#-observabilidad-y-trazabilidad)

---

## 🏗️ Arquitectura y Decisiones Técnicas

El proyecto se fundamenta en la **solidez arquitectónica** y la **observabilidad**, implementando patrones de diseño avanzados para sistemas de IA:

### 1. Orquestación Dinámica (Supervisor Pattern)
Se ha implementado un **Strategic Orchestrator (Manager Agent)** que actúa como el núcleo de decisión del grafo. Este componente evalúa dinámicamente el estado de la consulta, decide qué experto debe intervenir y gestiona las dependencias del flujo mediante aristas condicionales (`conditional_edges`).

#### 📊 Diagrama del Grafo de Orquestación
![Flujo de Orquestación](../assets/diagrama_orquestacion.png)

> **Nota:** Este diagrama ilustra el flujo de decisiones del supervisor, la delegación a expertos y el bucle de revisión de calidad antes de la persistencia del estado en SQLite.

### 2. Roles Profesionales Especializados
El sistema cuenta con roles claramente diferenciados para evitar solapamientos y maximizar el rigor técnico:
* **Market Intelligence Agent (Domain Expert):** Analiza el encaje de mercado, objetivos estratégicos y entorno competitivo.
* **Solutions Architect Agent (Technical Architect):** Define el stack tecnológico (especializado en .NET 8), evalúa la viabilidad técnica y propone la infraestructura.
* **Risk Officer Agent (Risk & Compliance):** Identifica riesgos normativos (GDPR), de ejecución y de seguridad en el procesamiento de datos.
* **Executive Reviewer (Critic):** Realiza el control de calidad final, consolidando las partes en un informe jerárquico y asignando un **Quality Score**.

### 3. Persistencia de Estado mediante Checkpointers
A diferencia de sistemas stateless, NSE integra una capa de persistencia robusta utilizando `SqliteSaver` de LangGraph. En la compilación del grafo, se inyecta un `checkpointer` que permite:
* **Trazabilidad Inmutable:** Cada transición entre nodos queda registrada en una base de datos SQLite local.
* **Aislamiento de Sesiones:** El uso de `thread_id` permite mantener múltiples conversaciones independientes con persistencia de memoria a largo plazo.
* **Resiliencia:** Capacidad de recuperar el estado exacto del grafo ante interrupciones del servicio.

---

## 🛠️ Stack Tecnológico
* **Backend:** Python 3.11+, FastAPI (Uvicorn), LangGraph, LangChain.
* **IA:** Modelos de OpenAI (GPT-4o / GPT-4o-mini).
* **Frontend:** Angular 18+ (Dashboard reactivo con observabilidad de procesos).
* **Infraestructura:** Docker & Docker Compose.

> **Nota Técnica:** El sistema inicializa automáticamente la base de datos de persistencia en `backend/data/nexus_strategy.db` al arrancar.

---

## 🚀 Instalación y Ejecución

El sistema permite dos modos de despliegue: mediante contenedores (recomendado) o ejecución manual en entorno local.

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd Nexus-Strategy-Engine
```

## 2. Configuración de Variables de Entorno

Crea un archivo llamado `.env` dentro de la carpeta `backend/` con el siguiente contenido:

```env
OPENAI_API_KEY="tu_api_key_aquí"
```

### 3. Ejecución con Docker (Recomendado)
Desde la terminal en la raíz del proyecto, ejecuta:

```bash
docker-compose up --build
```

> **Nota:** Este comando compilará el Frontend (Angular + Nginx) y preparará el Backend (FastAPI + LangGraph) con su persistencia SQLite.

### 4. Ejecución Local (Backend)

1. **Crear y activar el entorno virtual:**
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Lanzar el servidor FastAPI (desde la raíz del proyecto):**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚠️ Ajuste de Rutas e Importaciones (Importante)

Se han configurado las importaciones como **rutas absolutas de paquete**:

* **Ejecución Correcta:** El comando de arranque debe lanzarse siempre desde la **raíz del proyecto**.
* **Estructura:** Tanto en `main.py` como en los agentes, se utilizan rutas del tipo:

```python
from backend.agents.orchestrator import ...
```

> **Nota:** Si recibes un `ModuleNotFoundError`, asegúrate de **no** estar dentro de la carpeta `backend/`. El servidor necesita visibilidad de todo el árbol para gestionar la lógica correctamente.

---

## 🌐 Acceso al Sistema
* **Frontend (UI):** [http://localhost:4200](http://localhost:4200)
* **API (Docs/Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Ejemplos de Uso y Validación Técnica
Prueba estos casos en **Swagger** (`/docs`) para activar los flujos del grafo:

### 1. Estrategia de Expansión (Negocio + Riesgos)
**Input (JSON):**
```json
{
  "user_input": "Analiza la viabilidad de expandir nuestros servicios de consultoría de IA al mercado alemán. Considera la competencia local y el cumplimiento estricto de GDPR.",
  "thread_id": "expansion_alemania_001"
}
```

**Flujo esperado:** Orchestrator → Market Intelligence → Risk Officer.

### 2. Migración Tecnológica (Arquitectura)
**Input (JSON):**

```json
{
  "user_input": "Queremos migrar nuestra arquitectura legacy a un sistema basado en microservicios con .NET 8 y agentes autónomos. ¿Es técnicamente viable?",
  "thread_id": "migracion_dotnet_002"
}
```

**Flujo esperado:** Orchestrator → Solutions Architect.

---

### 🔄 Prueba de Persistencia (Seguimiento)
**Nexus Strategy Engine** tiene memoria de estado. Si usas el mismo `thread_id`, el sistema construye sobre lo ya aprendido.

**Input de Seguimiento (Mismo ID):**

```json
{
  "user_input": "Sobre la plataforma anterior, dame más detalles técnicos sobre la implementación del motor de scoring en .NET 8.",
  "thread_id": "migracion_dotnet_002"
}
```

**Comportamiento:** El Orchestrator detecta el contexto previo en SQLite y el **Solutions Architect** profundiza en detalles técnicos específicos sin repetir la información inicial.

---

## 📈 Interpretación de Resultados (Logs del Servidor)
El servidor expone logs en tiempo real para la **observabilidad**:

* **`[ORCHESTRATOR DECISION]`**: Nodo experto seleccionado por el supervisor para la tarea actual.
* **`[REASONING]`**: Justificación lógica del supervisor antes de delegar la tarea, detallando por qué ese experto es necesario.
* **`Quality Score`**: Puntuación final (0-10) asignada por el **Executive Reviewer** basada en la coherencia y rigor del informe.

---

## 📊 Observabilidad y Trazabilidad
Para garantizar la transparencia en los procesos de decisión, el sistema implementa tres niveles de auditoría:

* **Trazas de Decisión (Reasoning):** Registro del razonamiento interno antes de cada transición entre nodos, permitiendo reconstruir la lógica de orquestación.
* **Output Estructurado:** Informe final en **Markdown jerárquico** donde cada sección identifica de forma explícita al agente responsable.
* **Validación de Calidad:** Generación de un **Score de Validación** que certifica el rigor del resultado final.

**Ejemplo de salida en consola:**
```text
[ORCHESTRATOR DECISION] -> Delega a 'Market Intelligence'
[REASONING] -> El usuario solicita un análisis de mercado en Alemania, requiere validación de contexto local.
[AGENT_OUTPUT] -> Generando sección: Análisis de Competencia...
[QUALITY SCORE] -> 9/10
```

#### 📊 Diagrama de Flujo de Datos (Observabilidad)
![Secuencia de Observabilidad](../assets/diagrama_observabilidad.png)

> **Nota:** El sistema registra cada paso del razonamiento (`REASONING`) y los resultados intermedios (`AGENT_OUTPUT`), permitiendo una trazabilidad completa del proceso de IA hasta el informe final.

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **CC BY-NC-ND 4.0**. Se permite su visualización y descarga con fines exclusivamente académicos y de evaluación técnica. Queda prohibida cualquier explotación comercial o distribución de versiones derivadas.

---
**Desarrollado por Jorge Herráiz.**
