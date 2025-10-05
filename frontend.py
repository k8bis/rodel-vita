from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_BASE = "http://localhost:8001"  # Tu FastAPI

@app.route('/')
def dashboard():
    return render_template('dashboard.html')  # Si tienes, o redirige a especialistas

@app.route('/especialistas')
def especialistas():
    response = requests.get(f"{API_BASE}/especialistas/")
    data = response.json() if response.ok else []
    return render_template('especialistas.html', especialistas=data)

@app.route('/especialistas/create', methods=['POST'])
def create_especialista():
    # Fix: Lee form data (no JSON), convierte a dict
    data = dict(request.form)  # Convierte form a dict simple
    response = requests.post(f"{API_BASE}/especialistas/", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/pacientes')
def pacientes():
    # Nueva ruta para pacientes (similar)
    response = requests.get(f"{API_BASE}/pacientes/")
    data = response.json() if response.ok else []
    return render_template('pacientes.html', pacientes=data)

@app.route('/pacientes/create', methods=['POST'])
def create_paciente():
    data = dict(request.form)
    response = requests.post(f"{API_BASE}/pacientes/", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/reportes')
def reportes():
    # Ejemplo: Reporte para paciente ID 1 (hardcodea o usa input)
    response = requests.get(f"{API_BASE}/reportes/paciente/1")
    data = response.json() if response.ok else {}
    return render_template('reportes.html', reporte=data)

# Agrega más rutas similares para citas, reportes, etc.

if __name__ == '__main__':
    app.run(debug=True, port=5000)