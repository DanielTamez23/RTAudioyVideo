from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import pandas as pd
import os
import requests

app = Flask(__name__)

app.secret_key = "supersecreto"  # Aquí puedes poner una clave secreta única y segura

# Ruta del archivo Excel
EXCEL_FILE = "reparaciones.xlsx"

# Función para guardar datos en Excel
def guardar_en_excel(datos):
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    else:
        df = pd.DataFrame([datos])

    df.to_excel(EXCEL_FILE, index=False)

# Función para enviar correo utilizando Mailgun API
def enviar_correo(datos):
    API_KEY = "4cff576d549ae6d9ff83072e336f4ee4-f6202374-2b4cb6b0"  # Reemplaza con tu API Key de Mailgun
    DOMAIN = "sandboxcc309873941a425d99842f800d7d6a41.mailgun.org"  # Reemplaza con tu dominio Mailgun

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

    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data={
            "from": f"Mailgun Sandbox <postmaster@{DOMAIN}>",
            "to": "danieltamezmtz@hotmail.com",  # Reemplaza con tu correo
            "subject": subject,
            "text": body
        })

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
