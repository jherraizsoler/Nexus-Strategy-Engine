
# 🖥️ Nexus Strategy Dashboard (Frontend)

Este es el módulo de interfaz de usuario de **Nexus Strategy Engine**, una aplicación SPA desarrollada en **Angular 18** diseñada para la interacción en tiempo real con el hub de agentes estratégicos.

⬅️ **[Volver al README Principal](../README.md)**

---

## 📌 Índice
1. [🚀 Propósito del Módulo](#-propósito-del-módulo)
2. [🛠️ Stack Tecnológico](#️-stack-tecnológico)
3. [🏗️ Estructura del Proyecto](#️-estructura-del-proyecto)
4. [⚙️ Instalación y Desarrollo](#️-instalación-y-desarrollo)
    * [1. Instalación de Dependencias](#1-instalación-de-dependencias)
    * [2. Servidor de Desarrollo](#2-servidor-de-desarrollo)
    * [3. Compilación (Producción)](#3-compilación-producción)
5. [⚠️ Configuración de la API](#️-configuración-de-la-api)
6. [🧪 Pruebas y Scaffolding](#-pruebas-y-scaffolding)

---


## 🚀 Propósito del Módulo
La interfaz proporciona un entorno premium para la toma de decisiones, permitiendo:
* **Gestión de Consultas:** Entrada de prompts estratégicos y control de hilos (`thread_id`).
* **Visualización Dinámica:** Renderizado de informes técnicos mediante Markdown jerárquico.
* **Observabilidad del Proceso:** Feedback visual sobre el agente que está operando en cada momento.



---

## 🛠️ Stack Tecnológico
* **Core:** Angular 18+
* **Lenguaje:** TypeScript
* **Estilos:** SCSS (Arquitectura modular)
* **Librerías Clave:**
    * `ngx-markdown`: Para el renderizado profesional de los informes de los agentes.
    * `RxJS`: Gestión de flujos de datos asíncronos con el backend.
    * `HttpClient`: Comunicación con la API de FastAPI.

---

## 🏗️ Estructura del Proyecto
El frontend sigue una estructura organizada por responsabilidades:

* **`/src/app/services`**: Contiene la lógica de comunicación con el motor de IA.
* **`/src/app/components`**: Componentes reutilizables para el chat, los reportes y los indicadores de carga.
* **`/src/app/models`**: Interfaces de TypeScript para garantizar el tipado estricto de las respuestas del backend.

---

## ⚙️ Instalación y Desarrollo

### Requisitos Previos
* **Node.js**: v18.x o superior.
* **Angular CLI**: v18.x.

### 1. Instalación de Dependencias
Desde la carpeta `/frontend`, ejecuta:
```bash
npm install
```
### 2. Servidor de Desarrollo
Ejecuta el siguiente comando para iniciar el entorno local:

```bash
ng serve
```

Navega a `http://localhost:4200/`. La aplicación se recargará automáticamente si modificas el código fuente.

### 3. Compilación (Producción)
Para generar los artefactos de despliegue en la carpeta `dist/`:

```bash
ng build --configuration production
```

## ⚠️ Configuración de la API
La aplicación está configurada para conectarse al backend en `http://localhost:8000`.

* **Si utilizas Docker:** La comunicación está preconfigurada mediante el proxy interno.
* **Si ejecutas en local:** Asegúrate de que el backend esté activo antes de lanzar el frontend para evitar errores de conexión (CORS).

---

## 🧪 Pruebas y Scaffolding

### Generar Componentes
```bash
ng generate component components/nuevo-componente
```

### Ejecutar Tests
```bash
# Unit Tests
ng test

# E2E Tests
ng e2e
```
---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **CC BY-NC-ND 4.0**. Se permite su visualización y descarga con fines exclusivamente académicos y de evaluación técnica. Queda prohibida cualquier explotación comercial o distribución de versiones derivadas.

---
**Desarrollado por Jorge Herráiz.**