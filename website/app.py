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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:BUYBKZ7G5c1Mmh1Gg9xX@database-1.chduhfhuptun.us-east-1.rds.amazonaws.com/accounts'
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

@app.route('/home')
def home():
    if 'loggedin' in session:
        user = session['username']
        flash(f"Bienvenido {user}","info")
        return render_template('home.html')
    
    return redirect(url_for('index'))

@app.route('/movies')
def movies():
    if 'loggedin' in session:
        user = session['username']
        
        movie_id = request.args.get('movie_id')
        response = requests .get(f"http://34.201.109.22:8006/media/{movie_id}")

        if (response.status_code == 200):
            json_response = response.json()
        elif (response.status_code == 404):
            print("El servidor no ha encontrado el articulo buscado")
        else:
            print("Error desconocido!")



        flash(f"Vamos a ver una peli! {user}","info")
        return render_template('visual.html', json_response=json_response)
    
    return redirect(url_for('index'))


@app.errorhandler(IndexError)
def _indexError(err):
    return render_template("Error.html",err = err)
@app.errorhandler(ValueError)
def _valueError(err):
    return render_template("Error.html",err = err)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000 ,debug=True)
