from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import pandas as pd
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecreto")

# Ruta del archivo Excel
EXCEL_FILE = "reparaciones.xlsx"

# Credenciales y alcance de acceso
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Función para guardar datos en Excel
def guardar_en_excel(datos):
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    else:
        df = pd.DataFrame([datos])
    df.to_excel(EXCEL_FILE, index=False)

# Función para obtener el servicio de Gmail
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

# Función para enviar correo utilizando la API de Gmail
def enviar_correo(datos):
    service = get_gmail_service()
    subject = "Nueva solicitud de reparación"
    body = f"""
    Se ha recibido una nueva solicitud de reparación:
    
    Nombre: {datos['Nombre']}
    Teléfono WhatsApp: {datos['Teléfono WhatsApp']}
    Correo: {datos['Correo']}
    Categoría: {datos['Categoría']}
    Marca: {datos['Marca']}
    Descripción: {datos['Descripción']}
    Hora de Envío: {datos['Hora de Envío']}
    """
    
    message = create_message("me", "danieltamezmtz@hotmail.com", subject, body)
    send_message(service, "me", message)

# Crear mensaje en formato MIME
def create_message(sender, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

# Enviar el mensaje a través de la API de Gmail
def send_message(service, sender, message):
    try:
        message = service.users().messages().send(userId=sender, body=message).execute()
        print(f'Mensaje enviado: {message["id"]}')
    except Exception as error:
        print(f'Error al enviar mensaje: {error}')

# Rutas en Flask
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/enviar_solicitud", methods=["POST"])
def enviar_solicitud():
    datos = {
        'Nombre': request.form['nombre'],
        'Teléfono WhatsApp': request.form['telefono'],
        'Correo': request.form['correo'],
        'Categoría': request.form['categoria'],
        'Marca': request.form['marca'],
        'Descripción': request.form['descripcion'],
        'Hora de Envío': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    guardar_en_excel(datos)
    enviar_correo(datos)
    flash("Solicitud enviada con éxito", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
