from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bcrypt import checkpw
import os

app = Flask(__name__)  # No necesitamos static_folder ni static_url_path
CORS(app, resources={r"/login": {"origins": "http://127.0.0.1:5000"}})

# Configuración de la conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Paraguas"
USER_COLLECTION_NAME = "usuarios"
MEDICAMENTOS_COLLECTION_NAME = "medicamentos"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION_NAME]
medicamentos_collection = db[MEDICAMENTOS_COLLECTION_NAME]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # Servir index.html desde la misma carpeta

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)  # Servir otros archivos estáticos (CSS, etc.)

@app.route('/Video/<path:filename>')
def serve_video(filename):
    return send_from_directory('Video', filename)  # Servir videos desde la carpeta Video

@app.route('/img/<path:filename>')
def serve_images(filename):
    return send_from_directory('img', filename)  # Servir imágenes desde la carpeta img

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"Intento de login para el usuario: {username}")
    print(f"Contraseña ingresada: {password}")

    if not username or not password:
        print("Error: Nombre de usuario y/o contraseña faltan")
        return jsonify({'error': 'Nombre de usuario y contraseña son requeridos'}), 400

    user = user_collection.find_one({'nombre_usuario': username})

    if user:
        print(f"Usuario encontrado en la base de datos: {user['nombre_usuario']}")
        if checkpw(password.encode('utf-8'), user['contrasena'].encode('utf-8')):
            print("Login exitoso")
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            print("Error: Contraseña incorrecta")
            return jsonify({'error': 'Contraseña incorrecta'}), 401
    else:
        print("Error: Usuario no encontrado")
        return jsonify({'error': 'Usuario no encontrado'}), 401

@app.route('/buscar_medicamentos')
def buscar_medicamentos():
    # ... (código de buscar_medicamentos sin cambios)
    pass

if __name__ == '__main__':
    app.run(debug=True)