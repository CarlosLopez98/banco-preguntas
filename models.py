from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def get_modelo(entidad, datos=None):
    if datos == None:
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
        elif entidad == 'evaluaciones_preguntas':
            return evaluacion_pregunta
        elif entidad == 'tipo_preguntas':
            return tipo_pregunta
        elif entidad == 'preguntas':
            return pregunta
        elif entidad == 'respuestas':
            return respuesta
    else:
        if entidad == 'roles':
            return rol(rol_nombre=datos[0])
        elif entidad == 'usuarios':
            return usuario(usr_nombre=datos[0], usr_apellido=datos[1], usr_username=datos[2], 
                            usr_correo=datos[3], password=datos[4], usr_rol=datos[5])
        elif entidad == 'categorias':
            return categoria(cat_nombre=datos[0], cat_descripcion=datos[1])
        elif entidad == 'competencias':
            return competencia(com_nombre=datos[0], com_descripcion=datos[1], com_categoria=datos[2])
        elif entidad == 'evaluaciones':
            return evaluacion(eva_nombre=datos[0], eva_puntuacionmax=datos[1], eva_conjunta=datos[2], 
                                eva_usuario=datos[3])
        elif entidad == 'evaluaciones_preguntas':
            return evaluacion_pregunta(epr_evaluacion=datos[0], epr_pregunta=datos[1])
        elif entidad == 'tipo_preguntas':
            return tipo_pregunta(tpr_nombre=datos[0], tpr_descripcion=datos[1])
        elif entidad == 'preguntas':
            return pregunta(pre_texto=datos[0], pre_tipo_pregunta=datos[1], pre_competencia=datos[2],
                                pre_usuario=datos[3])
        elif entidad == 'respuestas':
            return respuesta(res_texto=datos[0], res_valor=datos[1], res_correcta=datos[2], res_pregunta=datos[3])


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

        return registro

    @classmethod
    def delete(cls, registro):
        db.session.delete(registro)
        db.session.commit()

#tabla rol
class rol(db.Model, modelo):
    __tablename__ = 'roles'
    
    id = db.Column('rol_id', db.Integer, primary_key=True)
    rol_nombre = db.Column(db.String(20), nullable=False, unique=True)
    usuarios = db.relationship('usuario', lazy='dynamic')
        
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
    usr_username = db.Column(db.String(50), nullable=False, unique=True)
    usr_correo = db.Column(db.String(100), nullable=False, unique=True)
    usr_contrasena = db.Column(db.String(94), nullable=False)
    usr_rol = db.Column(db.Integer, db.ForeignKey('roles.rol_id'))

    def __str__(self):
        return f'{self.usr_nombre.capitalize()} {self.usr_apellido.capitalize()} (@{self.usr_username.capitalize()})'

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'usr_id':
            return self.id
        elif atr == 'usr_nombre':
            return self.usr_nombre
        elif atr == 'usr_apellido':
            return self.usr_apellido
        elif atr == 'usr_username':
            return self.usr_username
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
    def create_element(cls, nombre, apellido, username, email, password, rol):
        user = usuario(usr_nombre=nombre, usr_apellido=apellido, usr_username=username, 
                        usr_correo=email, password=password, usr_rol=rol)

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get_by_username(cls, username):
        return usuario.query.filter_by(usr_username=username).first()

    @classmethod
    def get_by_email(cls, usr_correo):
        return usuario.query.filter_by(usr_correo=usr_correo).first()

    
#tabla de categoria
class categoria(db.Model, modelo):
    __tablename__ = 'categorias'

    id = db.Column('cat_id', db.Integer, primary_key = True)
    cat_nombre = db.Column(db.String(100), nullable=False)
    cat_descripcion = db.Column(db.Text, nullable=False)
    competencias = db.relationship('competencia', lazy='dynamic')

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'cat_id':
            return self.id
        elif atr == 'cat_nombre':
            return self.cat_nombre
        elif atr == 'cat_descripcion':
            return self.cat_descripcion

    @classmethod
    def create_element(cls, data):
        #FIX IT
        data[1]=get_modelo('niveles_categorias').get_by_name(data[1]).get_atr("nivel_id")
        
        if data[1]==1:
            r=None 
            
        else:
            r=get_modelo('categorias').get_by_name(data[2]).get_atr("cat_id")
            
        
        cat = categoria(cat_nombre=data[0],cat_nivel=data[1],cat_padre=r)

        db.session.add(cat)
        db.session.commit()

        return cat
        
        
#tabla para manejar competencias
class competencia(db.Model, modelo):
    __tablename__ = 'competencias'

    id = db.Column('com_id', db.Integer, primary_key=True)
    com_nombre = db.Column(db.String(50), nullable=False)
    com_descripcion = db.Column(db.Text, nullable=False)
    com_categoria = db.Column(db.Integer, db.ForeignKey('categorias.cat_id'))
    preguntas = db.relationship('pregunta', lazy='dynamic')

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'com_id':
            return self.id
        elif atr == 'com_nombre':
            return self.com_nombre
        elif atr == 'com_descripcion':
            return self.com_descripcion
        elif atr == 'com_categoria':
            return self.com_categoria


class evaluacion(db.Model, modelo):
    __tablename__ = 'evaluaciones'

    id = db.Column('eva_id', db.Integer, primary_key=True)
    eva_nombre = db.Column(db.String(100))
    eva_puntuacionmax = db.Column(db.Integer)
    eva_conjunta = db.Column(db.Boolean)
    eva_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.usr_id'))

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'eva_id':
            return self.id
        elif atr == 'eva_nombre':
            return self.eva_nombre
        elif atr == 'eva_puntuacionmax':
            return self.eva_puntuacionmax
        elif atr == 'eva_conjunta':
            return self.eva_conjunta
        elif atr == 'eva_usuario':
            return self.eva_usuario
        
    @classmethod
    def create_element(cls, data):
        
        eva = evaluacion(nombre=data[0], puntuacion_max=data[1], conjunta=data[2], usuario=data[3])

        db.session.add(eva)
        db.session.commit()

        return eva

#tabla para el manejo de tipo de preguntas
class tipo_pregunta(db.Model, modelo):
    __tablename__ = 'tipo_preguntas'

    id = db.Column('tpr_id', db.Integer, primary_key=True)
    tpr_nombre = db.Column(db.String(50), nullable=False)
    tpr_descripcion = db.Column(db.Text)
    preguntas = db.relationship('pregunta', lazy='dynamic')

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'tpr_id':
            return self.id
        elif atr == 'tpr_nombre':
            return self.tpr_nombre
        elif atr == 'tpr_descripcion':
            return self.tpr_descripcion
           
    @classmethod
    def create_element(cls, data):
        
        tipo= tipo_pregunta(data[0],data[1])

        db.session.add(tipo)
        db.session.commit()

        return tipo    
        

#tabla intermediaria entre pregunta y evaluacion
class evaluacion_pregunta(db.Model,modelo):
    __tablename__ = 'evaluaciones_preguntas'

    id = db.Column('epr_id', db.Integer, primary_key=True)
    epr_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluaciones.eva_id'))
    epr_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.pre_id'))
    epr_valor = db.Column(db.Integer, nullable=True)

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'epr_id':
            return self.id
        elif atr == 'epr_evaluacion':
            return self.epr_evaluacion
        elif atr == 'epr_pregunta':
            return self.epr_pregunta
        elif atr == 'epr_valor':
            return self.epr_valor


class pregunta(db.Model, modelo):
    __tablename__ = 'preguntas'
    __table_args__ = {'extend_existing': True}

    id = db.Column('pre_id', db.Integer, primary_key=True)
    pre_texto = db.Column(db.String(200))
    pre_tipo_pregunta = db.Column(db.Integer, db.ForeignKey('tipo_preguntas.tpr_id'))
    pre_competencia = db.Column(db.Integer, db.ForeignKey('competencias.com_id'))
    pre_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.usr_id'))
    respuestas = db.relationship('respuesta', lazy='dynamic')

    def __str__(self):
        return self.pre_texto

    # Obtener un atributo
    def get_atr(self, atr):
        if atr == 'pre_id':
            return self.id
        elif atr == 'pre_texto':
            return self.pre_texto
        elif atr == 'pre_tipo_pregunta':
            return self.pre_tipo_pregunta
        elif atr == 'pre_competencia':
            return self.pre_competencia
        elif atr == 'pre_usuario':
            return self.pre_usuario
        elif atr == 'pre_evaluacion':
            return self.pre_evaluacion
        
    @classmethod
    def create_element(cls, data):
        pass
    
#tala para manejo de respuesta
class respuesta(db.Model, modelo):
    __tablename__ = 'respuestas'
    

    id = db.Column('res_id', db.Integer, primary_key=True)
    res_texto = db.Column(db.String(140))
    res_correcta = db.Column(db.Boolean, nullable=False)
    res_valor = db.Column(db.Float)
    res_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.pre_id'))

    def get_atr(self,atr):
        if atr == 'res_id':
            return self.id
        elif atr == 'res_texto':
            return self.res_texto
        elif atr == 'res_correcta':
            return self.res_correcta
        elif atr == 'res_valor':
            return self.res_valor
        elif atr == 'res_pregunta':
            return self.res_pregunta

    @classmethod
    def create_element(cls, data):
        pass
