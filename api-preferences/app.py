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
            database="masterPro",
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




@app.route('/preference/<int:id_account>' , methods=["GET","POST", "PUT"])
def preference(id_account):

	conn = db_connection()
	cur = conn.cursor()

	if request.method == "GET":
		cur.execute(f"select * from preferences where id = {id_account}")
		rows = cur.fetchall()
		prefer = ""
		for row in rows:
			prefer = row
		if (prefer):
			return jsonify(prefer),200
		else:
			return jsonify("NOT FOUND"), 404

#a route with all the neccesary request methods for a single student	


@app.route('/like/<int:id_user>/<int:id_movie>' , methods=["GET","POST", "PUT"])
def like(id_user, id_movie):

    conn = db_connection()
    cur = conn.cursor()
    var = f'"{id_movie}"'
    cur.execute(f"INSERT INTO preferences (id, color_hex, favorites) VALUES ({id_user}, '#5639bf'::text, '[{var}]') ON CONFLICT (id) DO UPDATE SET favorites = preferences.favorites || '[{var}]'::jsonb;")
    conn.commit()

    return '', 204



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8010, debug=True)
