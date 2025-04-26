from pymongo import MongoClient
from bcrypt import hashpw, gensalt

MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/Paraguas?retryWrites=true&w=majority"
DB_NAME = "Paraguas"
USER_COLLECTION_NAME = "usuarios"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION_NAME]

# Credenciales de prueba
nombre_usuario_prueba = "Jloyo"
contrasena_prueba = "2580"

# Generar el salt y hashear la contraseña
salt = gensalt()
hashed_password = hashpw(contrasena_prueba.encode('utf-8'), salt)

# Crear el documento del usuario
usuario_prueba = {
    "nombre": "Jorge",
    "apellido": "Loyo",
    "lugar_de_trabajo": "Desarrollo",  # Ejemplo
    "mail": "jloyo@example.com",           # Ejemplo
    "contrasena": hashed_password.decode('utf-8'),
    "nombre_usuario": nombre_usuario_prueba
}

# Insertar el usuario en la colección
try:
    user_collection.insert_one(usuario_prueba)
    print(f"Usuario de prueba '{nombre_usuario_prueba}' insertado correctamente.")
except Exception as e:
    print(f"Error al insertar el usuario de prueba: {e}")

client.close()