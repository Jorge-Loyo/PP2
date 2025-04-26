from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
CORS(app)  # Para permitir solicitudes desde el frontend en desarrollo

# Configuración de la conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/mi_aplicacion_db?retryWrites=true&w=majority"
DB_NAME = "Paraguas"
USER_COLLECTION_NAME = "usuarios"
MEDICAMENTOS_COLLECTION_NAME = "medicamentos"  # Agrega el nombre de la colección de medicamentos

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION_NAME]
medicamentos_collection = db[MEDICAMENTOS_COLLECTION_NAME]  # Accede a la colección de medicamentos

@app.route('/')
def index():
    return send_file('menu.html') # Asegúrate de que 'menu.html' esté en el mismo directorio o ajusta la ruta

@app.route('/menu.html')
def menu():
    return send_file('menu.html') # Asegúrate de que 'menu.html' esté en el mismo directorio o ajusta la ruta

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Nombre de usuario y contraseña son requeridos'}), 400

    user = user_collection.find_one({'nombre_usuario': username})

    if user:
        if checkpw(password.encode('utf-8'), user['contrasena'].encode('utf-8')):
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'error': 'Contraseña incorrecta'}), 401
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 401

@app.route('/buscar_medicamentos')
def buscar_medicamentos():
    query = request.args.get('q')
    if query and len(query) >= 2:
        # Crear un patrón de búsqueda para que coincida con el inicio del nombre (insensible a mayúsculas/minúsculas)
        search_pattern = f"^{query}"
        medicamentos = medicamentos_collection.find(
            {'medicamento': {'$regex': search_pattern, '$options': 'i'}},
            {'_id': 0, 'medicamento': 1, 'laboratorio': 1, 'monodroga': 1,
             'prese_monodroga': 1, 'código_medicamento': 1, 'categorías': 1,
             'subcategoría': 1, 'TRAZABILIDAD': 1}
        ).limit(10)

        medicamentos_list = list(medicamentos)
        # Renombrar las claves para que coincidan con el frontend (opcional)
        formatted_medicamentos = []
        for med in medicamentos_list:
            formatted_medicamentos.append({
                'nombre': med.get('medicamento'),
                'laboratorio': med.get('laboratorio'),
                'monodroga': med.get('monodroga'),
                'presentacion': med.get('prese_monodroga'),
                'codigo': med.get('código_medicamento'),
                'grupo1': med.get('categorías'),  # Ajusta esto si 'categorías' corresponde a 'Grupo 1'
                'grupo2': med.get('subcategoría'), # Ajusta esto si 'subcategoría' corresponde a 'Grupo 2'
                'trazable': med.get('TRAZABILIDAD', False)
            })

        return jsonify(formatted_medicamentos)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)