from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bcrypt import checkpw
import os

app = Flask(__name__, static_folder='../frontend/Umbrella', static_url_path='/')
CORS(app, resources={r"/login": {"origins": "http://127.0.0.1:5000"}}) # Ajusta el origen si es necesario

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
    return send_file(os.path.join(app.static_folder, 'index.html'))

@app.route('/index.html')
def serve_index():
    return send_file(os.path.join(app.static_folder, 'index.html'))

@app.route('/menu.html')
def menu():
    return send_file(os.path.join(app.static_folder, 'menu.html'))

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
    query = request.args.get('q')
    if query and len(query) >= 2:
        search_pattern = f"^{query}"
        medicamentos = medicamentos_collection.find(
            {'medicamento': {'$regex': search_pattern, '$options': 'i'}},
            {'_id': 0, 'medicamento': 1, 'laboratorio': 1, 'monodroga': 1,
             'prese_monodroga': 1, 'código_medicamento': 1, 'categorías': 1,
             'subcategoría': 1, 'TRAZABILIDAD': 1}
        ).limit(10)

        medicamentos_list = list(medicamentos)
        formatted_medicamentos = []
        for med in medicamentos_list:
            formatted_medicamentos.append({
                'nombre': med.get('medicamento'),
                'laboratorio': med.get('laboratorio'),
                'monodroga': med.get('monodroga'),
                'presentacion': med.get('prese_monodroga'),
                'codigo': med.get('código_medicamento'),
                'grupo1': med.get('categorías'),
                'grupo2': med.get('subcategoría'),
                'trazable': med.get('TRAZABILIDAD', False)
            })

        return jsonify(formatted_medicamentos)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)