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
        cursor.execute('SELECT p.comentario, p.added_on, c.username FROM Puntuacion p INNER JOIN cuentas c ON p.id_usuario = c.id_cuentas WHERE p.id_pelicula = %s', (peliculaId,) )
        comments = cursor.fetchall()
        cursor.close()
        return jsonify(comments), 200
    except Exception as e:
        print('Error fetching comments:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Agregar un comentario
@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Puntuacion (id_pelicula, id_usuario, comentario) VALUES (%s, %s, %s)', (data[0], data[1], data[2]))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Comentario agregado correctamente.'}), 201
    except Exception as e:
        print('Error al agregar comentario:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Eliminar un comentario


if __name__ == '__main__':
    port = 3000
    app.run(host='0.0.0.0', port=port)
    print(f'Microservicios escuchando en el puerto {port}')