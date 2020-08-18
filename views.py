from flask import request, flash, url_for, redirect, render_template
from main import app, db, inspector
from models import *

@app.route('/')
def home():
	entidades = db.engine.table_names()
	return render_template('home.html', entidades = entidades)

@app.route('/list/<entidad>')
def list(entidad):
	campos = inspector.get_columns(entidad)
	return render_template('list.html', entidad = entidad, campos = campos )