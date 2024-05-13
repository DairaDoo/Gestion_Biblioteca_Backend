import sys
from flask import Flask, jsonify, request
import mariadb
from config import DATABASE_CONFIG
from flask_cors import CORS

# CORS permite que nuestro servidor Flask acepte solicitudes
# desde otros dominios, facilitando la interacción con
# aplicaciones web externas.

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos
try:
    connection = mariadb.connect(**DATABASE_CONFIG)
    cursor = connection.cursor()
except mariadb.Error as e:
    print(f"Error al conectarse a la base de datos MariaDB: {e}")
    sys.exit(1)

@app.route('/', methods=["GET"])
def hello_world():
    """Ruta de prueba para verificar que el servidor está funcionando."""
    return '¡Hola, mundo!'


@app.route('/api/getUsuarios', methods=["GET"])
def get_usuarios():
    """Obtiene todos los usuarios de la base de datos y los devuelve como JSON."""
    try:
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except mariadb.Error as e:
        error_message = f"Error al ejecutar la consulta SQL para obtener usuarios: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    

@app.route('/api/getLibros', methods=["GET"])
def get_libros():
    """Obtiene todos los libros de la base de datos y los devuelve como JSON."""
    try:
        cursor.execute("SELECT * FROM Libros")
        libros = cursor.fetchall()
        return jsonify(libros)
    except mariadb.Error as e:
        error_message = f"Error al ejecutar la consulta SQL para obtener libros: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    

@app.route('/api/getPrestamos', methods=["GET"])
def get_prestamos():
    """Obtiene todos los préstamos de la base de datos y los devuelve como JSON."""
    try:
        cursor.execute("SELECT * FROM Prestamos")
        prestamos = cursor.fetchall()
        return jsonify(prestamos)
    except mariadb.Error as e:
        error_message = f"Error al ejecutar la consulta SQL para obtener préstamos: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    

@app.route('/api/getCategorias', methods=["GET"])
def get_categorias():
    """Obtiene todas las categorías de la base de datos y las devuelve como JSON."""
    try:
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        return jsonify(categorias)
    except mariadb.Error as e:
        error_message = f"Error al ejecutar la consulta SQL para obtener categorías: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    
@app.route('/api/crearLibro', methods=["POST"])
def insert_new_user():
    """inserta un libro a la base de datos Usuarios."""
    try:
        query = "INSERT INTO Libros (Titulo, Autor, id_categoria) VALUES ('DummieBook', 'Dummie', 1)"
        cursor.execute(query)
        connection.commit()
        
        return "Libro agregado exitosamente!"
    
    except mariadb.Error as e:
        print("Error:", e)
        return "Error al agregar el libro a la base de datos.", 500
    
@app.route('/api/crearUsuario', methods=["POST"])
def insert_new_book():
    """inserta un usuario a la base de datos Usuarios."""
    try:
        query = "INSERT INTO Usuarios (nombre) VALUES ('DummieUser2')"
        cursor.execute(query)
        connection.commit()
        
        return "Usuario agregado exitosamente!"
    
    except mariadb.Error as e:
        print("Error:", e)
        return "Error al agregar el usuario a la base de datos.", 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
