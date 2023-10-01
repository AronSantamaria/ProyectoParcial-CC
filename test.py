from flask import Flask, request,jsonify, render_template
import  json
import psycopg2


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

conn = db_connection()
cur = conn.cursor()


cur.execute(f"select * from portada where id IN (100007,100008, 100009);")
rows = cur.fetchall()
movies = list()
for row in rows:
    movies.append(row)

            
if (movies):
    print(movies)
else:
    print("NOT FOUND")