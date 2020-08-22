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

    def get_atr(self,atr):
        pass

    @classmethod
    def get_by_id(cls, entidad, id):
        return entidad.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls, entidad):
        return entidad.query.all()

    @classmethod
    def add(cls, registro):
        db.session.add(registro)
        db.session.commit()

    @classmethod
    def delete(cls, registro):
        db.session.delete(registro)
        db.session.commit()

#tabla rol

class rol(db.Model, modelo):
    __tablename__ = 'roles'

    id = db.Column('rol_id', db.Integer, primary_key=True)
    rol_nombre = db.Column(db.String(20), nullable=False)

    def __init__(self, nombre):
        self.rol_nombre = nombre
        
    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'rol_id':
            return self.id
        elif atr == 'rol_nombre':
            return self.rol_nombre
    @classmethod
    def get_by_name(cls, rol_nombre):
        return rol.query.filter_by(rol_nombre=rol_nombre).first()
#tabla usuario
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
       
        return check_password_hash(self.usr_contrasena, password)

    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.usr_contrasena = generate_password_hash(value)
        
    @classmethod
    def create_element(cls, nombre,apellido,email,password,rol):
        user = usuario(usr_nombre=nombre,usr_apellido=apellido,usr_correo=email,usr_contrasena=password,usr_rol=rol)

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get_by_id(cls, id):
        return usuario.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, usr_nombre):
        return usuario.query.filter_by(usr_nombre=usr_nombre).first()

    @classmethod
    def get_by_email(cls, usr_correo):
        return usuario.query.filter_by(usr_correo=usr_correo).first()     
        
#tabla nivel categoria

class nivel_categoria(db.Model,modelo):
    __tablename__='niveles_categorias'
    
    id= db.Column('nivel_id', db.Integer , primary_key = True)
    nivel_nombre=db.column(db.String(50))
    
    def __init__(self, nombre):
        self.nivel_nombre_nombre = nombre

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'nivel_id':
            return self.id
        elif atr == 'nivel_nombre':
            return self.nivel_nombre


    
#tabla de categoria
class categoria(db.Model, modelo):
    __tablename__ = 'categorias'

    id = db.Column('cat_id', db.Integer, primary_key = True)
    cat_padre=db.column(db.Integer,db.ForeignKey('categorias.id'))
    cat_nivel=db.column(db.Integer,db.ForeignKey('niveles_categorias.id'))
    cat_nombre = db.Column(db.String(100))

    def __init__(self, nombre,cat_nivel):
        self.cat_nombre = nombre
        self.cat_nivel=cat_nivel

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'cat_id':
            return self.id
        elif atr == 'cat_nombre':
            return self.cat_nombre
        elif atr=='cat_nivel':
            return self.cat_nivel
        elif atr=='cat_padre':
            return self.cat_padre




#Tabla intermediaria entre categoria y competencia
class categoria_competecia(db.Model,modelo):
    __tablename__='categorias_competencias'
    
    id=db.Column('catCom',db.Integer,primary_key=True)
    cat_id=db.column(db.Integer,db.ForeignKey('categorias.id'))
    com_id=db.column(db.Integer,db.ForeignKey('competencias.id'))
    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'cat_com_id':
            return self.id
        elif atr == 'cat_id':
            return self.cat_id
        elif atr== 'com_id':
            return self.com_id
        
        
        
#tabla para manejar competencias
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

#tabla conexion entre evaluacion y competencia

class evaluacion_competencia(db.Model,modelo):
    __tablename__='evaluaciones_competencias'

    id=db.Column('eva_com_id', db.Integer, primary_key=True)        
    eva_id=db.column(db.Integer,db.ForeignKey('evaluaciones.id'))
    com_id=db.column(db.Integer,db.ForeignKey('competencias.id'))
    
    def __init__(self,eva_id,com_id):
        self.eva_id=eva_id
        self.com_id=com_id
        
        
    def get_atr(self,atr):
        if atr=='eva_id':
            return self.eva_id
        elif atr=='com_id':
            return self.com_id
#tabla para manejo de evaluacion


class evaluacion(db.Model, modelo):
    __tablename__ = 'evaluaciones'

    id = db.Column('eva_id', db.Integer, primary_key=True)
    eva_nombre = db.Column(db.String(100))
    eva_puntuacionmax = db.Column(db.Integer)
    eva_conjunta = db.Column(db.Boolean)
    eva_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.usr_id'))
    eva_competencia = db.Column(db.Integer, db.ForeignKey('competencias.com_id'))

    def __init__(self, nombre, puntuacion_max, usuario, competencia, conjunta=False):
        self.eva_nombre = nombre
        self.eva_puntuacionmax = puntuacion_max
        self.eva_conjunta = conjunta
        self.eva_usuario = usuario
        self.eva_competencia = competencia

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
        elif atr == 'eva_competencia':
            return self.eva_competencia

#tabla para el manejo de tipo de preguntas
class tipo_pregunta(db.Model, modelo):
    __tablename__ = 'tipo_preguntas'

    id = db.Column('tpr_id', db.Integer, primary_key=True)
    tpr_nombre = db.Column(db.String(50), nullable=False)
    tpr_descripcion = db.Column(db.Text)

    def __init__(self, nombre, descripcion=None):
        self.tpr_nombre = nombre
        self.tpr_descripcion = descripcion

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'tpr_id':
            return self.id
        elif atr == 'tpr_nombre':
            return self.tpr_nombre
        elif atr == 'tpr_descripcion':
            return self.tpr_descripcion

#tabla intermediaria entre pregunta y evaluacion
class evaluacion_pregunta(db.Model,modelo):
    __tablename__='evaluaciones_preguntas'
    id = db.Column('pre_eva_id', db.Integer, primary_key = True)
    eva_id=db.column(db.Integer,db.ForeignKey('evaluaciones.id'))
    pre_id=db.column(db.Integer,db.ForeignKey('preguntas.id'))
    
    def __init__(self, eva_id,pre_id):
        self.eva_id = eva_id
        self.pre_id=pre_id

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'eva_pre_id':
            return self.id
        elif atr == 'eva_id':
            return self.eva_id
        elif atr == 'pre_id':
            return self.pre_id
    
#tabla para manejo de tipo de preguntas
class pregunta(db.Model, modelo):
    __tablename__ = 'preguntas'

    id = db.Column('pre_id', db.Integer, primary_key = True)
    pre_texto = db.Column(db.String(150))
    pre_tipo_pregunta = db.Column(db.Integer, db.ForeignKey('tipo_preguntas.tpr_id'))

    def __init__(self, texto,  tipo):
        self.pre_texto = texto
        self.pre_tipo_pregunta = tipo

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'pre_id':
            return self.id
        elif atr == 'pre_texto':
            return self.pre_texto
        elif atr == 'pre_tipo_pregunta':
            return self.pre_tipo_pregunta
        

#tala para manejo de respuesta
class respuesta(db.Model, modelo):
    __tablename__ = 'respuestas'

    id = db.Column('res_id', db.Integer, primary_key=True)
    res_texto = db.Column(db.String(140))
    res_valor = db.Column(db.Float)
    res_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.pre_id')) #Revisar

    def __init__(self, texto, valor, pregunta):
        self.res_texto = texto
        self.res_valor = valor
        self.res_pregunta = pregunta

    def get_atr(self,atr):
        if atr == 'res_id':
            return self.id
        elif atr == 'res_texto':
            return self.res_texto
        elif atr == 'res_valor':
            return self.res_valor
        elif atr == 'res_pregunta':
            return self.res_pregunta