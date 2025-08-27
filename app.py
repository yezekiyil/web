from flask import Flask, render_template_string, request, redirect, url_for
import qrcode
import io
import base64

app = Flask(__name__)

# Almacenamiento simple en memoria
asistencias = []

# Página principal con QR
@app.route('/')
def index():
    # Cambia '192.168.1.100' por la IP de tu PC en la red local
    qr_data = 'http://192.168.1.2:5000/formulario'
    qr_img = qrcode.make(qr_data)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render_template_string('''
        <h1>Escanea el código QR para registrar tu asistencia</h1>
        <img src="data:image/png;base64,{{img_base64}}">
        <br><a href="{{ url_for('asistencia') }}">Ver asistencia</a>
    ''', img_base64=img_base64)

# Formulario de asistencia
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        curso = request.form['curso']
        asistencias.append({'nombre': nombre, 'apellido': apellido, 'curso': curso})
        return redirect(url_for('asistencia'))
    return render_template_string('''
        <h2>Formulario de Asistencia</h2>
        <form method="post">
            Nombre: <input name="nombre" required><br>
            Apellido: <input name="apellido" required><br>
            Curso: <input name="curso" required><br>
            <button type="submit">Registrar</button>
        </form>
    ''')

# Listado de asistencias
@app.route('/asistencia')
def asistencia():
    return render_template_string('''
        <h2>Listado de Asistencias</h2>
        <table border="1">
            <tr><th>Nombre</th><th>Apellido</th><th>Curso</th></tr>
            {% for a in asistencias %}
            <tr>
                <td>{{a.nombre}}</td>
                <td>{{a.apellido}}</td>
                <td>{{a.curso}}</td>
            </tr>
            {% endfor %}
        </table>
        <br><a href="{{ url_for('index') }}">Volver</a>
    ''', asistencias=asistencias)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)