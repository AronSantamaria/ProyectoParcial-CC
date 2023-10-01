from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura la conexión a PostgreSQL
db_config = {
    "user": "postgres",
    "password": "BUYBKZ7G5c1Mmh1Gg9xX",
    "host": "database-1.chduhfhuptun.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "masterPro"
}

conn = psycopg2.connect(**db_config)

# Obtener comentarios por película
@app.route('/comments/<int:peliculaId>', methods=['GET'])
def get_comments(peliculaId):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT comentario, added_on, id_usuario FROM Puntuacion WHERE id_pelicula = %s', (peliculaId,))
        comments = cursor.fetchall()
        cursor.close()
        return jsonify(comments), 200
    except Exception as e:
        print('Error fetching comments:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Agregar un comentario
@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    peliculaId = data.get('id_movie')
    usuarioId = data.get('id_cuenta')
    comentario = data.get('comentario')
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Puntuacion (id_pelicula, id_usuario, comentario) VALUES (%s, %s, %s)', (peliculaId, usuarioId, comentario))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Comentario agregado correctamente.'}), 201
    except Exception as e:
        print('Error al agregar comentario:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Eliminar un comentario
@app.route('/comments/<int:peliculaId>/<int:usuarioId>', methods=['DELETE'])
def delete_comment(peliculaId, usuarioId):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Puntuacion WHERE id_pelicula = %s AND id_usuario = %s', (peliculaId, usuarioId))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Comentario eliminado correctamente.'}), 200
    except Exception as e:
        print('Error al eliminar comentario:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Actualizar un comentario
@app.route('/comments/<int:peliculaId>/<int:usuarioId>', methods=['PUT'])
def update_comment(peliculaId, usuarioId):
    data = request.get_json()
    nuevoComentario = data.get('nuevoComentario')
    
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE Puntuacion SET comentario = %s WHERE id_pelicula = %s AND id_usuario = %s', (nuevoComentario, peliculaId, usuarioId))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Comentario actualizado correctamente.'}), 200
    except Exception as e:
        print('Error al actualizar comentario:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    port = 3000
    app.run(host='0.0.0.0', port=port)
    print(f'Microservicios escuchando en el puerto {port}')