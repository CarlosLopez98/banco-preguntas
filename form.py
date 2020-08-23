from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField, IntegerField,SelectField,FloatField
from wtforms.fields.html5 import EmailField

from models import *
from main import inspector 


def getForm(form,r):
    if form =='categorias':
        return CategoriaForm(r,niveles=0)
    elif form == 'competencias':
        return CompetenciaForm(r)
    elif form=='evaluaciones':
        return EvaluacionForm(r)
    elif form =='preguntas':
        return PreguntaForm(r,tipos=0)
    elif form =='tipo_preguntas':
        return TipoPreguntaForm(r)
    elif form =='respuestas':
        return RespuestaForm(r,preguntas=0)
    
def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar este registro!')
        
class LoginForm(Form):
    email = StringField('Username', [
        validators.length(min=4, max=50, message='El campo debe tener entre 4 y 50 caracteres.'),
    ])
    password = PasswordField('Password', [
        validators.Required(message='El password es requerido.'),
    ])       
    
    
class RegisterForm(Form):
    nombre = StringField('Nombre', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa tu nombre.')
    ])
    
    
    apellido = StringField('Primer apellido', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa tu apellido.')
    ])
    
  
    
    email = EmailField('Email', [
     validators.length(min=6, max=100, message='El campo debe tener entre 4 y 50 caracteres.'),
     validators.Required(message='El email es requerido.'),
     validators.Email(message='Ingrese un email válido.')
    ])
    password = PasswordField('Password', [
        validators.Required(message='El password es requerido.'),
        validators.EqualTo('confirm_password', message='La contraseña no coincide')
    ])
    confirm_password = PasswordField('Confirm password')
    
    rol=get_modelo('roles').get_all(get_modelo('roles'))
    roles=SelectField('roles', choices=[(r.get_atr('rol_nombre')) for r in rol ])
    
    honeypot = HiddenField('', [ lenght_honeypot])


    def validate_username(self, username):
        if usuario.get_by_username(username.data):
            raise validators.ValidationError('El username ya se encuentra registrado.')

    def validate_email(self, email):
        if usuario.get_by_email(email.data):
            raise validators.ValidationError('El email ya se encuentra registrado.')

    # Sobreescritura del metodo validate
    def validate(self):
        if not Form.validate(self):
            return False

        # Validaciones propias
        if len(self.password.data) < 4:
            self.password.errors.append('El password es demasiado corto.')
            return False

        return True    
    
    
class CategoriaForm(Form):
    nombre=  StringField('Nombre de la categoria', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])  
    nivel=get_modelo('niveles_categorias').get_all(get_modelo('niveles_categorias'))
    niveles=SelectField('niveles de categoria', choices=[(n.get_atr('nivel_nombre')) for n in nivel ])
    
    padre=get_modelo('categorias').get_by_nivel(1)
   
    padres=SelectField('Espacios academicos', choices=[(pa.get_atr('cat_nombre')) for pa in padre])
    
    def validate(self):
        if not Form.validate(self):
            return False
        return True
class CompetenciaForm(Form):
    nombre= StringField('Nombre de la competencia', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])

    descripcion= StringField('descripcion', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])     
    
class EvaluacionForm(Form):
       nombre= StringField('Nombre de la evaluación', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])  
       
       valor= IntegerField('Valor maximo', [
       validators.data_required(message='Ingresa un valor.')
    ])  
       conjunta = BooleanField()
       com=get_modelo('competencias').get_all(get_modelo('competencias'))
       competencias=SelectField('Competencia', choices=[(t.get_atr('com_nombre')) for t in com])
       
class PreguntaForm(Form):
        contenido= StringField('Contenido de la pregunta', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])    
        tipo=get_modelo('tipo_preguntas').get_all(get_modelo('tipo_preguntas'))
        tipos=SelectField('Tipos de pregunta', choices=[(t.get_atr('tpr_nombre')) for t in tipo])
        
class TipoPreguntaForm(Form):
        contenido= StringField('Nombre', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ]) 
        descripcion= StringField('Descripción', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa una descripcion.')
    ]) 
        
class RespuestaForm(Form):
    texto=StringField('Texto', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ])    
    
    valor=FloatField('valor', [
        
        validators.data_required(message='Ingresa un nombre.')
    ])    
    
    pregunta=get_modelo('preguntas').get_all(get_modelo('preguntas'))
    preguntas=SelectField('preguntas', choices=[(p.get_atr('pre_texto')) for p in pregunta ])
    
    