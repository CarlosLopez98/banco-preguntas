from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField, IntegerField,SelectField,FloatField
from wtforms.fields.html5 import EmailField
from models import *


def getForm(form, r):
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
    email = StringField('Correo', [
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
    username = StringField('Nombre de usuario', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa un nombre de usuario.')
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
    
    rol = get_modelo('roles').get_all(get_modelo('roles'))
    roles = SelectField('Roles', choices=[(r.id, r.rol_nombre) for r in rol])
    
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
    nombre = StringField('Nombre de la categoría', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Nombre de la competencia'})
    descripcion = TextAreaField('Descripción de la categoría', [
        validators.data_required(message='Ingresa una descripción')
    ], render_kw={'rows': 4, 'placeholder': 'Descripción de la categoría'})
    
    def validate(self):
        if not Form.validate(self):
            return False
        return True


class CompetenciaForm(Form):
    nombre = StringField('Nombre de la competencia', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Nombre de la competencia'})

    descripcion = TextAreaField('Descripción', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'rows': 4, 'placeholder': 'Descripción de la competencia'})

    categories = get_modelo('categorias').get_all(get_modelo('categorias'))
    categorias = SelectField('Categoria', choices=[(categorie.id, categorie.cat_nombre) for categorie in categories])


class EvaluacionForm(Form):
    nombre = StringField('Nombre de la evaluación', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Escribe un nombre para la evaluación'})  

    valor = IntegerField('Calificación máxima', [
        validators.data_required(message='Ingresa un valor.')
    ])  
    conjunta = BooleanField('Es conjunta', render_kw={'style': 'width: 20px'})


class PreguntaForm(Form):
    contenido = StringField('Contenido de la pregunta', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Escribe el contenido de la pregunta'})

    tipo = get_modelo('tipo_preguntas').get_all(get_modelo('tipo_preguntas'))
    tipos = SelectField('Tipos de pregunta', choices=[(t.id, t.tpr_nombre) for t in tipo])

    competencia = get_modelo('competencias').get_all(get_modelo('competencias'))
    competencias = SelectField('Competencias', choices=[(c.id, c.com_nombre) for c in competencia])


class TipoPreguntaForm(Form):
    contenido= StringField('Nombre', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Escribe el nombre del tipo'})
    descripcion= TextAreaField('Descripción', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa una descripcion.')
    ], render_kw={'placeholder': 'La descripción del tipo'}) 


class RespuestaForm(Form):
    texto = StringField('Texto', [
        validators.length(min=4, max=50),
        validators.data_required(message='Ingresa el nombre.')
    ], render_kw={'placeholder': 'Escribe el texto de la respuesta'})    
    
    valor = FloatField('Valor', [
        validators.data_required(message='Ingresa un valor.')
    ], render_kw={'placeholder': 'Que valor tiene la respuesta'})

    correcta = BooleanField('Correcta', render_kw={'style': 'width: 20px;'})
    
    pregunta = get_modelo('preguntas').get_all(get_modelo('preguntas'))
    preguntas = SelectField('preguntas', choices=[p.pre_texto for p in pregunta ])

    def actualizar(self):
        self.pregunta = get_modelo('preguntas').get_all(get_modelo('preguntas'))
        self.preguntas = SelectField('preguntas', choices=[p.pre_texto for p in self.pregunta ])
