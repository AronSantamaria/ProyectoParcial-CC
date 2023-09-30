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


@app.route('/skinners' , methods=["GET","POST", "PUT"])
def skinners():

    conn = db_connection()
    cur = conn.cursor()

    if request.method == "GET":
        lista = request.get_json()
        cur.execute(f"SELECT id, tittle, poster, likes_, rating FROM portada WHERE id IN ({', '.join(map(str, lista))})")
        rows = cur.fetchall()

        skin = list()
        for row in rows:
            skin.append(row)


        if (skin):
            return jsonify(skin),200
        else:
            return jsonify("NOT FOUND"), 404

#a route with all the neccesary request methods for a single student	


@app.route('/search' , methods=["GET","POST", "PUT"])
def search():
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "GET":
        lista = request.get_json()
        request_1 = ', '.join([' \'%'+palabra.lower()+'%\' ' for palabra in lista])
        cur.execute(f"select id, tittle, poster, likes_, rating from portada where (tittle || description) ILIKE ANY(ARRAY[{request_1}]);")
        rows = cur.fetchall()

        skin = list()
        for row in rows:
            skin.append(row)


        if (skin):
            return jsonify(skin),200
        else:
            return jsonify("NOT FOUND"), 404


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8006, debug=True)
