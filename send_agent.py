import base64
import os
import requests
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from zoneinfo import ZoneInfo

# Librerías de Google
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# --- CONFIGURACIÓN Y CONSTANTES ---
MADRID_TZ = ZoneInfo("Europe/Madrid")
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
]

class MailingAgent:
    def __init__(self, spreadsheet_id, ai_api_url=None, ai_api_key=None):
        self.spreadsheet_id = spreadsheet_id
        self.ai_url = ai_api_url
        self.ai_key = ai_api_key
        self.creds = self._get_google_creds()
        self.gmail = build("gmail", "v1", credentials=self.creds)
        self.sheets = build("sheets", "v4", credentials=self.creds)
        self.calendar = build("calendar", "v3", credentials=self.creds)

    def _get_google_creds(self):
        if os.path.exists("token.json"):
            return Credentials.from_authorized_user_file("token.json", SCOPES)
        return None

    def load_rows_from_sheet(self, sheets_service):
        """Lee las filas de la pestaña AGENT (Columnas A a N)."""
        try:
            # Adaptado a tu captura: Pestaña AGENT, columnas A hasta N
            range_name = "AGENT!A:N" 
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, 
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return [], []
                
            header = values[0] 
            rows = []
            
            for i, row in enumerate(values[1:], start=2):
                row_dict = {header[j]: row[j] if j < len(row) else "" for j in range(len(header))}
                row_dict['_sheet_row'] = i 
                rows.append(row_dict)
                
            return rows, header
        except Exception as e:
            print(f"Error en load_rows_from_sheet: {e}")
            return [], []

    def add_new_row(self, data_dict):
        """Añade una nueva empresa al final de la pestaña AGENT."""
        try:
            # Definimos el orden exacto de tus columnas según la imagen
            header = [
                "ENTERPRISE", "CONTACT_NAME", "EMAIL", "LANG", "TEMPLATE_ID", 
                "CUSTOM_LINE", "SUBJECT", "ATTACH_CV", "ATTACH_COVER", "STATUS"
            ]
            
            # Creamos la lista de valores respetando ese orden
            new_row = [data_dict.get(col, "") for col in header]
            
            body = {'values': [new_row]}
            self.sheets.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="AGENT!A:J", # Escribimos las primeras 10 columnas principales
                valueInputOption="RAW",
                body=body
            ).execute()
            return True
        except Exception as e:
            print(f"Error al añadir fila: {e}")
            return False

    def create_email_draft(self, to, subject, body, attachments=None):
        msg = EmailMessage()
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        if attachments:
            for path in attachments:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        msg.add_attachment(
                            f.read(), 
                            maintype="application", 
                            subtype="pdf", 
                            filename=os.path.basename(path)
                        )
        
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        return self.gmail.users().drafts().create(
            userId="me", 
            body={"message": {"raw": raw_message}}
        ).execute()

    def main(self):
        print("🤖 Iniciando proceso de envío del Agente...")
        # Aquí puedes añadir tu lógica para leer STATUS == 'READY' y enviar.
        pass