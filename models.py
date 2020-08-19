from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def get_modelo(entidad):
    if entidad == 'roles':
        return rol
    elif entidad == 'usuarios':
        return usuario
    elif entidad == 'categorias':
        return categoria
    elif entidad == 'tipo_categorias':
        return tipo_categoria
    elif entidad == 'competencias':
        return competencia
    elif entidad == 'evaluaciones':
        return evaluacion
    elif entidad == 'tipo_preguntas':
        return tipo_pregunta
    elif entidad == 'preguntas':
        return pregunta
    elif entidad == 'respuestas':
        return respuesta


class modelo:

    def get_atr(self):
        pass

    @classmethod
    def get_by_id(cls, entidad, id):
        return entidad.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls, entidad):
        return entidad.query.all()


class rol(db.Model, modelo):
    __tablename__ = 'roles'

    id = db.Column('rol_id', db.Integer, primary_key=True)
    rol_nombre = db.Column(db.String(20), nullable=False)

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'rol_id':
            return self.id
        elif atr == 'rol_nombre':
            return self.rol_nombre
    

class usuario(db.Model, modelo, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column('usr_id', db.Integer, primary_key=True)
    usr_nombre = db.Column(db.String(50), nullable=False)
    usr_apellido = db.Column(db.String(50), nullable=False)
    usr_correo = db.Column(db.String(100), nullable=False, unique=True)
    usr_contrasena = db.Column(db.String(94), nullable=False)
    usr_rol = db.Column(db.Integer, db.ForeignKey('roles.rol_id'))

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'usr_id':
            return self.id
        elif atr == 'usr_nombre':
            return self.usr_nombre
        elif atr == 'usr_apellido':
            return self.usr_apellido
        elif atr == 'usr_correo':
            return self.usr_correo
        elif atr == 'usr_rol':
            return self.usr_rol

    def verify_password(self, password):
        return check_password_hash(self.contrasena, password)

    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.contrasena = generate_password_hash(value)


class categoria(db.Model, modelo):
    __tablename__ = 'categorias'

    id = db.Column('cat_id', db.Integer, primary_key = True)
    cat_nombre = db.Column(db.String(100))
    cat_tipo = db.Column(db.Integer, db.ForeignKey('tipo_categorias.tca_id'))

    def __init__(self, nombre, tipo):
        self.cat_nombre = nombre
        self.cat_tipo = tipo

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'cat_id':
            return self.id
        elif atr == 'cat_nombre':
            return self.cat_nombre
        elif atr == 'cat_tipo':
            return self.cat_tipo


class tipo_categoria(db.Model, modelo):
    __tablename__ = 'tipo_categorias'

    id = db.Column('tca_id', db.Integer, primary_key = True)
    tca_nombre = db.Column(db.String(50))

    def __init__(self, nombre):
        self.tca_nombre = nombre

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'tca_id':
            return self.id
        elif atr == 'tca_nombre':
            return self.tca_nombre


class competencia(db.Model, modelo):
    __tablename__ = 'competencias'

    id = db.Column('com_id', db.Integer, primary_key=True)
    com_nombre = db.Column(db.String(50))
    com_descripcion = db.Column(db.Text)

    def __init__(self, nombre, descripcion):
        self.com_nombre = nombre
        self.com_descripcion = descripcion

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'com_id':
            return self.id
        elif atr == 'com_nombre':
            return self.com_nombre
        elif atr == 'com_descripcion':
            return self.com_descripcion


class evaluacion(db.Model, modelo):
    __tablename__ = 'evaluaciones'

    id = db.Column('eva_id', db.Integer, primary_key=True)
    eva_nombre = db.Column(db.String(100))
    eva_puntuacionmax = db.Column(db.Integer)
    eva_conjunta = db.Column(db.Boolean)
    eva_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.usr_id'))

    def __init__(self, nombre, puntuacion_max, conjunta=False):
        self.eva_nombre = nombre
        self.eva_puntuacionmax = puntuacion_max
        self.conjunta = conjunta

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'eva_id':
            return self.id
        elif atr == 'eva_nombre':
            return self.eva_nombre
        elif atr == 'eva_puntacionmax':
            return self.eva_puntacionmax
        elif atr == 'eva_conjunta':
            return self.eva_conjunta
        elif atr == 'eva_usuario':
            return self.eva_usuario


class tipo_pregunta(db.Model, modelo):
    __tablename__ = 'tipo_preguntas'

    id = db.Column('tpr_id', db.Integer, primary_key=True)
    tpr_mombre = db.Column(db.String(50))
    tpr_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluaciones.eva_id'))

    def __init__(self, nombre):
        self.tpr_nombre = nombre

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'tpr_id':
            return self.id
        elif atr == 'tpr_nombre':
            return self.tpr_nombre
        elif atr == 'tpr_evaluacion':
            return self.tpr_evaluacion    


class pregunta(db.Model, modelo):
    __tablename__ = 'preguntas'

    id = db.Column('pre_id', db.Integer, primary_key = True)
    pre_texto = db.Column(db.String(150))
    pre_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluaciones.eva_id'))
    pre_categoria = db.Column(db.Integer, db.ForeignKey('categorias.cat_id')) 
    pre_competencia = db.Column(db.Integer, db.ForeignKey('competencias.com_id'))
    pre_tipo_pregunta = db.Column(db.Integer, db.ForeignKey('tipo_preguntas.tpr_id'))

    def __init__(self, texto, categoria, tipo, competencia):
        self.pre_texto = texto
        self.cat_id = categoria
        self.com_id = competencia
        self.tpr_id = tipo

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'pre_id':
            return self.id
        elif atr == 'pre_texto':
            return self.pre_texto
        elif atr == 'pre_evaluacion':
            return self.pre_evaluacion
        elif atr == 'pre_categoria':
            return self.pre_categoria
        elif atr == 'pre_competencia':
            return self.pre_competencia
        elif atr == 'pre_tipo_pregunta':
            return self.pre_tipo_pregunta
        


class respuesta(db.Model, modelo):
    __tablename__ = 'respuestas'

    id = db.Column('res_id', db.Integer, primary_key=True)
    res_texto = db.Column(db.String(140))
    res_valor = db.Column(db.Float)
    res_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.pre_id')) #Revisar

    def __init__(self, texto, valor, pregunta):
        self.res_texto = texto
        self.res_valor = valor
        self.pre_id = pregunta

    def get_atr(self):
        if atr == 'res_id':
            return self.id
        elif atr == 'res_texto':
            return self.res_texto
        elif atr == 'res_valor':
            return self.res_valor
        elif atr == 'res_pregunta':
            return self.res_pregunta