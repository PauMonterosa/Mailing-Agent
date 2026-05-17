# Career Management System (CMS) - Applied Physics Engineering

Este repositorio contiene un agente de automatización de mailing diseñado para gestionar candidaturas de forma profesional. El sistema integra Google Sheets como base de datos, una interfaz interactiva en Streamlit y un motor de generación de texto técnico (LLM).

## 🛠️ Arquitectura del Sistema

1.  **Dashboard (Streamlit)**: Interfaz para visualización, filtrado y edición de candidaturas.
2.  **Mailing Agent (Backend)**: Conexión con la API de Google Sheets y gestión de envíos.
3.  **Generador IA**: Módulo de NLP para redactar párrafos técnicos personalizados.

## 📊 Configuración de la Base de Datos (Google Sheets)

Para que el sistema funcione, el Google Sheet vinculado debe tener la siguiente estructura de columnas (estrictamente en la primera fila):

| Columna | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **ENTERPRISE** | Nombre de la compañía | Hipra |
| **CONTACT_NAME** | Persona de contacto | Maria García |
| **EMAIL** | Email de destino | hr@empresa.com |
| **LANG** | Idioma del correo (ES, CA, EN) | EN |
| **TEMPLATE_ID** | Identificador de la plantilla | general_tech |
| **CUSTOM_LINE** | Párrafo generado o manual | Me interesa su división de fotónica... |
| **STATUS** | Estado (DRAFT, SENT, SCHEDULED) | DRAFT |

> **Nota**: El ID de la hoja se configura en la variable `SPREADSHEET_ID` dentro de `app.py`.

## 🚀 Instalación y Despliegue

### 1. Clonar y dependencias
```bash
git clone [https://github.com/PauMonterosa/Mailing-Agent.git](https://github.com/PauMonterosa/Mailing-Agent.git)
cd Mailing-Agent
pip install -r requirements.txt
```
### 2. Credenciales de Google
Es necesario obtener el archivo credentials.json desde la Google Cloud Console (habilitando la API de Google Sheets y Google Drive) y situarlo en la raíz del proyecto. El archivo token.json se generará automáticamente tras el primer inicio de sesión.

### 3. Ejecución
```bash
streamlit run app.py
```
## 🔧 Extensibilidad
El sistema es modular. La lógica de generación de texto está aislada en generar_texto_motivacional, permitiendo la migración a APIs oficiales de OpenAI o Anthropic de forma sencilla.

Autor: Pau Monterosa

Perfil: Ingeniería Física