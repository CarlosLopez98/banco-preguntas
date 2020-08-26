from flask import request, flash, url_for, redirect, render_template, abort, session
from main import app, db, inspector, login_manager
from models import *
from flask_login import login_user, logout_user, login_required, current_user
from form import *
import main
from models import *

@app.errorhandler(404)
def page_not_found(error):
	entidades = db.engine.table_names()
	return render_template('error404.html', title="Error 404", entidades=entidades), 404

@login_manager.user_loader
def load_user(id):
	return usuario.get_by_id(id)

@app.route('/')
@login_required
def home():
    
    entidades = db.engine.table_names()    
    return render_template('home.html', title='Inicio', menu='toggled', entidades=entidades)

@app.route('/list/<string:entidad>')
@login_required
def list(entidad):
	entidades = db.engine.table_names()
	campos = inspector.get_columns(entidad)

	if len(campos) == 0:
		abort(404)

	registros = get_modelo(entidad).get_all(get_modelo(entidad))

	return render_template('list.html', title=entidad, entidades=entidades, entidad=entidad, campos=campos, registros=registros)

@app.route('/add/<string:entidad>',methods=['GET', 'POST'])
@login_required
def add(entidad):
    entidades = db.engine.table_names()
        
    campos = inspector.get_columns(entidad)

    if len(campos) == 0:   
        abort(404)

    form=getForm(entidad,request.form)
    if entidad == 'respuestas':
        form.actualizar()

    if request.method == 'POST' and form.validate():
        data=[]
        for i in form:
            data+=[i.data]
        get_modelo(entidad).create_element(data)

        registros = get_modelo(entidad).get_all(get_modelo(entidad))
        flash('El registro se agregó con éxito', 'success')
        return render_template('list.html', title=entidad, entidades=entidades, entidad=entidad, campos=campos, registros=registros)
        
    return render_template('add.html', title=f'Añadir {entidad}', entidad=entidad, entidades=entidades,form=form)

@app.route('/edit/<string:entidad>/<int:id>')
@login_required
def edit(entidad, id):
	entidades = db.engine.table_names()
    
	return render_template('edit.html', title=f'Editar {entidad}', entidad=entidad, entidades=entidades)

@app.route('/delete/<string:entidad>/<int:id>')
@login_required
def delete(entidad, id):
	registro = get_modelo(entidad).get_by_id(get_modelo(entidad), id)
	if registro is None:
		flash('El registro que desea eliminar no existe', 'warning')
		session['message'] = 'El registro que desea eliminar no existe'
	else:
		registro.delete(registro)
		flash('El registro se eliminó con éxito', 'success')
		session['message'] = 'El registro se eliminó con éxito'

	return redirect(url_for('list', entidad=entidad))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.email.data
        password = form.password.data
        
        user = usuario.get_by_email(username)
        if user and user.verify_password(password):
            login_user(user)
            flash('Usuario autenticado.', 'success')

            return redirect(url_for('home'))

        else:
            flash('email o password incorrectos.', 'danger')
    
    return render_template('login.html', title="Ingresar",form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm(request.form,roles=1)
   
    if request.method == 'POST' and form.validate():
        name=form.nombre.data
        apellido=form.apellido.data
        email = form.email.data
        password = form.password.data
        r=form.roles.data
        r=rol.get_by_name(r).get_atr('rol_id')
        user = usuario.create_element(name,apellido,email,password,r)
        flash('Usuario registrado con éxito.', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Sesión cerrada con éxito', 'success')
    return redirect(url_for('login'))
	

