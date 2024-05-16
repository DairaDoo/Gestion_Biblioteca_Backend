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


@app.route('/api/borrarUsuario/<int:num_socio>', methods=["DELETE"])
def delete_user(num_socio):
    """Borra un usuario de la base de datos utilizando su ID y elimina los préstamos relacionados."""
    try:
        # Elimina los préstamos asociados al usuario
        query = "DELETE FROM Prestamos WHERE num_socio = ?"
        cursor.execute(query, (num_socio,))
        connection.commit()

        # Borra el usuario de la tabla de usuarios
        query = "DELETE FROM Usuarios WHERE num_socio = ?"
        cursor.execute(query, (num_socio,))
        connection.commit()

        return jsonify({'message': 'Usuario eliminado exitosamente'})

    except mariadb.Error as e:
        error_message = f"Error al eliminar usuario: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500


    

@app.route('/api/borrarLibro/<int:id_libro>', methods=["DELETE"])
def delete_book(id_libro):
    """Borra un libro de la base de datos utilizando su ID."""
    try:
        query = "DELETE FROM Libros WHERE id_libro = ?"
        cursor.execute(query, (id_libro, ))
        connection.commit()
        
        return jsonify({'message': 'Libro eliminado exitosamente'})
    
    except mariadb.Error as e:
        error_message = f"Error al eliminar usuario: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    
@app.route('/api/borrarPrestamo/<int:id_prestamo>', methods=["DELETE"])
def delete_prestamo(id_prestamo):
    """Borra un prestamo de la base de datos utilizando su ID."""
    try:
        query = "DELETE FROM Prestamos WHERE id_prestamo = ?"
        cursor.execute(query, (id_prestamo, ))
        connection.commit()
        
        return jsonify({'message': 'Prestamo eliminado exitosamente'})
    
    except mariadb.Error as e:
        error_message = f"Error al eliminar usuario: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    

@app.route('/api/borrarCategoria/<int:id_categoria>', methods=["DELETE"])
def delete_categoria(id_categoria):
    """Borra un prestamo de la base de datos utilizando su ID."""
    try:
        query = "DELETE FROM Categorias WHERE id_categoria = ?"
        cursor.execute(query, (id_categoria, ))
        connection.commit()
        
        return jsonify({'message': 'Categoria eliminada exitosamente'})
    
    except mariadb.Error as e:
        error_message = f"Error al eliminar categoria: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500

@app.route('/api/new_user', methods=['POST'])
def new_user():
    # Obtain JSON data from the request
    datos = request.json
    nombre = datos.get('nombre')
    
    # Insert the new user into the database
    strQry = 'INSERT INTO Usuarios (nombre) VALUES (?)'
    cursor.execute(strQry, (nombre,))
    connection.commit()

    # Return a JSON response indicating success
    response = {"message": "New user added successfully"}
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
