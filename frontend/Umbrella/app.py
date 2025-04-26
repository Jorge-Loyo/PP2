from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
CORS(app)  # Para permitir solicitudes desde el frontend en desarrollo

# Configuración de la conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/mi_aplicacion_db?retryWrites=true&w=majority"
DB_NAME = "Paraguas" 
USER_COLLECTION_NAME = "usuarios"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION_NAME]

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

if __name__ == '__main__':
    app.run(debug=True)