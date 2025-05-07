from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bcrypt import hashpw, checkpw, gensalt
import logging

app = Flask(__name__, template_folder='templates')
CORS(app)
app.logger.setLevel(logging.DEBUG)  # Habilita el logging de debug

# Configuración de la conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://Jloyo:2580@cluster0.rbb8srm.mongodb.net/mi_aplicacion_db?retryWrites=true&w=majority"
DB_NAME = "Paraguas"
USER_COLLECTION_NAME = "usuarios"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db[USER_COLLECTION_NAME]

@app.route('/', methods=['GET'])
def index():
    css_url = url_for('static', filename='styles.css')
    img_url = url_for('static', filename='logo sin fondo.png')
    app.logger.debug(f"Index - CSS URL: {css_url}")
    app.logger.debug(f"Index - Image URL: {img_url}")
    return render_template('Index.html', css_url=css_url, img_url=img_url)

@app.route('/login', methods=['POST'])
def login():
    # Placeholder logic for login
    return jsonify({"message": "Login endpoint is under construction"}), 200

@app.route('/menu', methods=['GET'])
def menu():
    css_url = url_for('static', filename='styles.css')
    menu_css_url = url_for('static', filename='menu.css')
    img_url = url_for('static', filename='logo sin fondo.png')
    app.logger.debug(f"Menu - CSS URL: {css_url}")
    app.logger.debug(f"Menu - Menu CSS URL: {menu_css_url}")
    app.logger.debug(f"Menu - Image URL: {img_url}")
    return render_template('menu.html', css_url=css_url, menu_css_url=menu_css_url, img_url=img_url)

# No necesitamos rutas explícitas para archivos estáticos aquí
# Flask los servirá automáticamente desde la carpeta 'static'
if __name__ == '__main__':
    app.run(debug=True)