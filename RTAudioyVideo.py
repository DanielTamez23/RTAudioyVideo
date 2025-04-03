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
app.secret_key = "supersecreto"  # Aquí puedes poner una clave secreta única y segura

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
            # Usamos las variables de entorno para las credenciales de cliente
            client_config = {
                "installed": {
                    "client_id": os.getenv('CLIENT_ID'),
                    "client_secret": os.getenv('CLIENT_SECRET'),
                    "project_id": os.getenv('PROJECT_ID'),
                    "auth_uri": os.getenv('AUTH_URI'),
                    "token_uri": os.getenv('TOKEN_URI'),
                    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
                    "redirect_uris": os.getenv('REDIRECT_URIS'),  # Asumiendo que es una lista separada por comas
                    "javascript_origins": os.getenv('JAVASCRIPT_ORIGINS')
                }
            }

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_console()
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    return service

# Función para enviar correo utilizando la API de Gmail
def enviar_correo(datos):
    service = get_gmail_service()  # Obtiene el servicio de Gmail

    subject = "Nueva solicitud de reparación"
    body = f"""
    Se ha recibido una nueva solicitud de reparación con los siguientes datos:

    Nombre: {datos['Nombre']}
    Teléfono WhatsApp: {datos['Teléfono WhatsApp']}
    Correo: {datos['Correo']}
    Categoría: {datos['Categoría']}
    Marca: {datos['Marca']}
    Descripción del problema: {datos['Descripción']}
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
        print('Mensaje enviado: %s' % message['id'])
        return message
    except Exception as error:
        print(f'Error al enviar mensaje: {error}')

# Ruta en Flask para manejar el formulario
@app.route("/enviar_solicitud", methods=["POST"])
def enviar_solicitud():
    if request.method == "POST":
        datos = {
            'Nombre': request.form['nombre'],
            'Teléfono WhatsApp': request.form['telefono'],
            'Correo': request.form['correo'],
            'Categoría': request.form['categoria'],
            'Marca': request.form['marca'],
            'Descripción': request.form['descripcion'],
            'Hora de Envío': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        guardar_en_excel(datos)  # Guardamos los datos en el archivo Excel
        enviar_correo(datos)  # Enviamos el correo con la información de la solicitud

        flash("Solicitud enviada con éxito", "success")
        return redirect(url_for("index"))  # Redirigir a la página principal

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/repair', methods=["GET", "POST"])
def repair():
    if request.method == "POST":
        nombre = request.form["nombre"]
        whatsapp = request.form["whatsapp"]
        correo = request.form["correo"]
        categoria = request.form["categoria"]
        marca = request.form["marca"]
        descripcion = request.form["descripcion"]

        # Guardar en Excel con la hora de envío
        datos = {
            "Nombre": nombre,
            "Teléfono WhatsApp": whatsapp,
            "Correo": correo,
            "Categoría": categoria,
            "Marca": marca,
            "Descripción": descripcion,
            "Hora de Envío": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual
        }
        
        # Guardar en Excel
        guardar_en_excel(datos)

        # Enviar correo
        try:
            response = enviar_correo(datos)
            if response.status_code == 200:
                print("Correo enviado correctamente")
            else:
                print(f"Error al enviar el correo: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

         # Mensaje flash para mostrar en la página
        flash("¡Se envió tu reporte correctamente! En poco tiempo nos contactaremos contigo.")
        return redirect(url_for('home'))  # Redirigir a la página de inicio

    return render_template("repair.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
