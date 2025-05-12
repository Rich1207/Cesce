from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

ARCHIVO_DATOS = 'solicitudes_cts.csv'

def inicializar_archivo():
    """Crea el archivo CSV con encabezados si no existe"""
    try:
        with open(ARCHIVO_DATOS, 'x', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                'Fecha_Hora',
                'Nombres',
                'Apellido_Paterno',
                'Apellido_Materno',
                'DNI',
                'Sueldo_Promedio',
                'Email'
            ])
    except FileExistsError:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    datos = {
        'fecha_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'nombres': request.form.get('nombres', '').strip(),
        'apellido_paterno': request.form.get('apellido_paterno', '').strip(),
        'apellido_materno': request.form.get('apellido_materno', '').strip(),
        'dni': request.form.get('dni', '').strip(),
        'sueldo': request.form.get('sueldo', '').strip(),
        'email': request.form.get('email', '').strip().lower()
    }

    errores = []
    
    # Validaciones
    if not datos['nombres']:
        errores.append("Nombres son obligatorios")
    if not datos['apellido_paterno']:
        errores.append("Apellido Paterno es obligatorio")
    if not datos['apellido_materno']:
        errores.append("Apellido Materno es obligatorio")
    if not datos['dni']:
        errores.append("DNI es obligatorio")
    elif not (datos['dni'].isdigit() and len(datos['dni']) == 8):
        errores.append("DNI debe ser numérico y tener 8 dígitos")
    if not datos['sueldo']:
        errores.append("Sueldo es obligatorio")
    else:
        try:
            float(datos['sueldo'])
        except ValueError:
            errores.append("Sueldo debe ser un número válido")
    if not datos['email']:
        errores.append("Email es obligatorio")
    elif '@' not in datos['email']:
        errores.append("Email debe ser válido")

    if errores:
        return render_template('index.html', errores=errores, datos=datos)

    # Guardar en CSV
    try:
        with open(ARCHIVO_DATOS, 'a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                datos['fecha_hora'],
                datos['nombres'],
                datos['apellido_paterno'],
                datos['apellido_materno'],
                datos['dni'],
                datos['sueldo'],
                datos['email']
            ])
    except Exception as e:
        return f"Error al guardar los datos: {str(e)}", 500

    return render_template('index.html',
        mensaje_exito="Solicitud procesada con éxito. En breve será enviada la simulación de CTS al correo electrónico proporcionado."
    )

if __name__ == '__main__':
    inicializar_archivo()
    app.run(debug=True)