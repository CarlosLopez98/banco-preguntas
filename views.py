from flask import request, flash, url_for, redirect, render_template, abort
from main import app, db, inspector, login_manager
from models import *
from flask_login import login_user, logout_user, login_required, current_user


@app.errorhandler(404)
def page_not_found(error):
	entidades = db.engine.table_names()
	return render_template('error404.html', title="Error 404", entidades=entidades), 404

@login_manager.user_loader
def load_user(id):
	return usuario.get_by_id(id)

@app.route('/')
def home():
	entidades = db.engine.table_names()
	return render_template('home.html', title='Inicio', menu='toggled', entidades=entidades)

@app.route('/list/<string:entidad>')
def list(entidad):
	entidades = db.engine.table_names()
	campos = inspector.get_columns(entidad)

	if len(campos) == 0:
		abort(404)

	registros = get_modelo(entidad).get_all(get_modelo(entidad))

	return render_template('list.html', title=entidad, entidades=entidades, entidad=entidad, campos=campos, registros=registros)

@app.route('/update/<string:entidad>/<int:id>')
def update(entidad, id):
	return 'h1'

@app.route('/login')
def login():
	return render_template('login.html', title="Ingresar")

@app.route('/signup')
def signup():
	return render_template('signup.html', title="Registro")