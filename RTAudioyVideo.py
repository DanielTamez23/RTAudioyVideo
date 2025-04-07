from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import pandas as pd
import os

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

        # Mensaje flash para mostrar en la página
        flash("¡Se envió tu reporte correctamente! En poco tiempo nos contactaremos contigo.")
        return redirect(url_for('home'))  # Redirigir a la página de inicio

    return render_template("repair.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
