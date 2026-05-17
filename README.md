# Career Management System (CMS) - Applied Physics Engineering

Este repositorio contiene un agente de automatización de mailing diseñado para optimizar y gestionar candidaturas profesionales. El sistema integra la gestión de bases de datos mediante Google Sheets, una interfaz de usuario interactiva con Streamlit y un módulo de generación de texto técnico mediante modelos de lenguaje (LLM).

## 🛠️ Arquitectura del Sistema

El proyecto se divide en tres pilares fundamentales:

1.  **Dashboard de Control (Streamlit)**: Interfaz de usuario que permite la visualización en tiempo real del estado de las candidaturas, búsqueda filtrada y previsualización de contenidos antes del envío.
2.  **Mailing Agent (Backend)**: Lógica encargada de la comunicación con la API de Google Sheets y el procesamiento de los estados de envío.
3.  **Generador Motivacional (IA)**: Módulo de procesamiento de lenguaje natural (NLP) que redacta párrafos técnicos personalizados basados en puntos clave y el perfil de la empresa.

## 🚀 Funcionalidades Clave

* **Matriz de Aplicaciones**: Visualización dinámica de empresas (fetch de logos vía Clearbit/Google) y estados de envío (DRAFT, SCHEDULED, SENT).
* **Laboratorio de Redacción**: Herramienta de generación de texto multi-idioma (Castellano, Català, English) con capacidad de edición en caliente.
* **Sincronización en Tiempo Real**: Conexión bidireccional con Google Sheets para persistencia de datos.

## 📋 Requisitos e Instalación

### Dependencias
El sistema requiere Python 3.8+ y las librerías listadas en `requirements.txt`.

```bash
pip install -r requirements.txt
```
### Configuración
Para el despliegue local, es necesario configurar las credenciales de Google Cloud (OAuth 2.0) y asignar el SPREADSHEET_ID correspondiente en el archivo principal.

## 🔧 Desarrollo y Extensibilidad
El código está estructurado para facilitar la implementación de nuevos módulos:

## IA: La lógica de generación se encuentra encapsulada en generar_texto_motivacional para facilitar la migración a otros modelos o APIs (OpenAI, Anthropic, etc.).

## Templates: El sistema soporta la inclusión de nuevas plantillas de correo en el backend del agente.

## Autor: Pau Monterosa

## Perfil: Ingeniería Física

"# Mailing-Agent" 
