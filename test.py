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

@app.route('/comments/<int:peliculaId>', methods=['GET'])
def get_comments(peliculaId):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Puntuacion WHERE id_pelicula = %s', (peliculaId,))
        comments = cursor.fetchall()
        cursor.close()
        return jsonify(comments), 200
    except Exception as e:
        print('Error fetching comments:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=3000, debug=True)