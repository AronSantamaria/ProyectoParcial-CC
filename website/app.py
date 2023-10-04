from operator import le
import re
from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, not_, or_, delete,select,update,values
from flask_migrate import Migrate
import sys
import json
import bcrypt
import requests



app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:BUYBKZ7G5c1Mmh1Gg9xX@database-1.chduhfhuptun.us-east-1.rds.amazonaws.com/masterPro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db) 

class Cuentas(db.Model):
    __tablename__ = 'cuentas'
    id_cuentas = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False, unique=True)


@app.route('/')
def index():
    with app.app_context():
        db.create_all()
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    _mail = request.form.get('mail')
    _password = request.form.get('password').encode('utf-8')
    results = Cuentas.query.filter_by(email=_mail)
    if(results.count() == 0):
        flash("Alguno(s) de los campos es vacio(s) o es erroneo(s)!","info")
        return redirect(url_for('index'))
    else:
        if bcrypt.checkpw(_password, results.first().password.encode('utf-8')):
            session['loggedin'] = True
            session['id'] = results.first().id_cuentas
            session['username'] = results.first().username
            return redirect(url_for('home'))
        else:
            flash("Uno de los campos es vacio o es erroneo!","info")
            return redirect(url_for('index'))
        
    
@app.route('/signup', methods=['POST'])
def signup():
    _username = request.form.get('username')
    _password = request.form.get('password').encode('utf-8')
    _password = bcrypt.hashpw(_password,bcrypt.gensalt()).decode('utf-8')
    _mail = request.form.get('mail')
    prueba1=Cuentas.query.filter_by(email=_mail)
    prueba2=Cuentas.query.filter_by(username=_username)
    prueba3=Cuentas.query.filter_by(password=_password)
    if (prueba1.count()==0 and prueba2.count()==0 and prueba3.count()==0):
        if (_username=='' or _password=='' or _mail==''):
            flash("Un campo es vacio! ","info")
            return redirect(url_for('register'))
        else:
            user = Cuentas(email=_mail,password=_password,username=_username)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    flash("Uno o mas campos ya estan registrados!","info")
    return redirect(url_for("register"))
            
@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        flash("You've been logged out!","info")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/registro')
def register():
    return render_template('register.html')

@app.route('/home' , methods=['POST', 'GET'] )
def home():
    if 'loggedin' in session:
        search = request.form.get('search')


        try:
            if (search is None or search == ""):
                #CONECTASE CON EL MICROSERVICIO DE PREFERENCIAS
                try:
                    response = requests.get(f"http://3.212.27.88:8010/preference/{session['id']}").json()
                    if(response == "NOT FOUND"):
                        response = []
                    else:
                        content = requests.get(f"http://3.212.27.88:8006/skinners", data=json.dumps(response[2]), headers={"Content-Type": "application/json"}).json()
                        flash(f"Tu color favorito es: ", response[1])
                        return render_template('home.html', mesg = ("Tus Favoritos  (" + str(len(content))) + "):", movie_list=content)
                except Exception as e:
                    pass
                

                flash("Aun no tenemos tus preferencias. Agrega algo!")
                return render_template('home.html', mesg = "Tus Favoritos  (0)" , movie_list=[])
                    

                
            else:
                content = requests.get(f"http://3.212.27.88:8006/search", data=json.dumps(search.split()), headers={"Content-Type": "application/json"})


                if content.status_code == 404:
                    return render_template('home.html', mesg = "No pudimos encontrar ningun resultado.", movie_list=content.json())
                else:
                    return render_template('home.html', mesg = "Resultados (" + str(len(content.json()))+ "):", movie_list=content.json())
        except requests.exceptions.ConnectTimeout as err:
            # Manejar el error de tiempo de conexión aquí
            return render_template("Error.html", err=err)     
        
    return redirect(url_for('index'))


@app.route('/selection', methods=['POST','GET'])
def selection():
    if 'loggedin' in session:
        identifier = int(request.args.get('identifier'))
        if(identifier == 0):
            response = requests.get(f"http://3.212.27.88:8010/preference/{session['id']}").json()
            if(response == "NOT FOUND"):
                content = []
            else:
                content = requests.get(f"http://3.212.27.88:8006/skinners", data=json.dumps(response[2]), headers={"Content-Type": "application/json"}).json()
                flash(f"Tu color favorito es: ", response[1])
            return render_template('home.html', mesg = ("Tus Favoritos  (" + str(len(content))) + "):", movie_list=content)

        else:
            content = requests.get(f"http://3.212.27.88:8006/movieseries/{identifier}").json()

        return render_template('home.html', mesg = "", movie_list=content)
        
    return redirect(url_for('index'))



@app.route('/movies')
def movies():
    if 'loggedin' in session:
        user = session['username']
        
        movie_id = request.args.get('movie_id')
        
        response = requests.get(f"http://3.212.27.88:8006/media/{movie_id}")

        if (response.status_code == 200):
            json_response = response.json()
        elif (response.status_code == 404):
            print("El servidor no ha encontrado el articulo buscado")
        else:
            print("Error desconocido!")

        comments = requests.get(f"http://3.212.27.88:3000/comments/{movie_id}").json()
            
        flash(f"Vamos a ver una peli! {user}","info")
        return render_template('visual.html', logcasual=comments , id_tocoment=movie_id , json_response=json_response[1], comentarios=comments)
    
    return redirect(url_for('index'))


@app.route('/coment', methods=['POST', 'GET'])
def coment():
    if 'loggedin' in session:
        id_cuenta = session['id']
        movie_id = request.form.get('movieIdField')
        comentario = request.form.get('comentario')
        datos = [movie_id, id_cuenta, str(comentario)]
        response = requests.post(f"http://3.212.27.88:3000/comment", data=json.dumps(datos), headers={"Content-Type": "application/json"})
        


        response = requests.get(f"http://3.212.27.88:8006/media/{(movie_id)}")
        if (response.status_code == 200):
            json_response = response.json()
        elif (response.status_code == 404):
            print("El servidor no ha encontrado el articulo buscado")
        else:
            print("Error desconocido!")


        comments = requests.get(f"http://3.212.27.88:3000/comments/{(movie_id)}").json()


        
        return render_template('visual.html', logcasual=json_response[1] , id_tocoment=movie_id , json_response=json_response[1], comentarios=comments)

    return redirect(url_for('index'))

@app.route('/like' , methods=["GET","POST", "PUT"])
def like():
    if 'loggedin' in session:
        requests.post(f"http://3.212.27.88:8010/like/{session['id']}/{request.args.get('movie_id')}")
        return '', 204


@app.errorhandler(IndexError)
def _indexError(err):
    return render_template("Error.html",err = err)
@app.errorhandler(ValueError)
def _valueError(err):
    return render_template("Error.html",err = err)
@app.errorhandler(requests.exceptions.ConnectTimeout)
def _indexError(err):
    return render_template("Error.html",err = err)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050 ,debug=True)
