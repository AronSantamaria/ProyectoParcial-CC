from flask import Flask, request,jsonify, render_template
import  json
import psycopg2

app = Flask(__name__)

#an in memory students storage(using a list)
#students = []
#instead of a list,we need to create a connection to database where we store students

def db_connection():
    conn = None
    try:
        # Reemplaza los valores con los de tu base de datos en Amazon RDS
        conn = psycopg2.connect(
            database="media",
            user="postgres",
            password="BUYBKZ7G5c1Mmh1Gg9xX",
            host="database-1.chduhfhuptun.us-east-1.rds.amazonaws.com",
            port="5432"  # El puerto predeterminado de PostgreSQL es 5432
        )
        if conn is not None:
            print("Conexión exitosa a la base de datos PostgreSQL")
        else:
            print("No se pudo establecer la conexión a la base de datos PostgreSQL")

    except psycopg2.Error as e:
        print(e)
    return conn




@app.route('/media/<int:id>' , methods=["GET","POST", "PUT"])
def media(id):

	conn = db_connection()
	cur = conn.cursor()

	if request.method == "GET":
		cur.execute(f"SELECT video FROM movies WHERE id={id}")
		rows = cur.fetchall()
		movies = ""
		for row in rows:
			movies = row
		if (movies):
			return jsonify(movies),200
		else:
			return jsonify("NOT FOUND"), 404

#a route with all the neccesary request methods for a single student	


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8006, debug=True)