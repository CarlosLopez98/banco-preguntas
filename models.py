from main import db


class categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column('cat_id', db.Integer, primary_key = True)
    cat_nombre = db.Column(db.String(100))
    cat_tipo = db.Column(db.Integer, db.ForeignKey('tipo_categorias.tca_id'))

    def __init__(self, nombre, tipo):
        self.cat_nombre = nombre
        self.cat_tipo = tipo


class tipo_categoria(db.Model):
    __tablename__ = 'tipo_categorias'

    id = db.Column('tca_id', db.Integer, primary_key = True)
    tca_nombre = db.Column(db.String(50))

    def __init__(self, nombre):
        self.tca_nombre = nombre


class competencia(db.Model):
    __tablename__ = 'competencias'

    id = db.Column('com_id', db.Integer, primary_key=True)
    com_nombre = db.Column(db.String(50))
    com_descripcion = db.Column(db.Text)

    def __init__(self, nombre, descripcion):
        self.com_nombre = nombre
        self.com_descripcion = descripcion


class evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column('eva_id', db.Integer, primary_key=True)
    eva_nombre = db.Column(db.String(100))
    eva_puntuacionmax = db.Column(db.Integer)
    eva_conjunta = db.Column(db.Boolean)

    def __init__(self, nombre, puntuacion_max, conjunta=False):
        self.eva_nombre = nombre
        self.eva_puntuacionmax = puntuacion_max
        self.conjunta = conjunta



class tipo_pregunta(db.Model):
    __tablename__ = 'tipo_preguntas'

    id = db.Column('tpr_id', db.Integer, primary_key=True)
    tpr_mombre = db.Column(db.String(50))
    eva_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.eva_id'))

    def __init__(self, nombre):
        self.tpr_nombre = nombre


class pregunta(db.Model):
    __tablename__ = 'preguntas'

    id = db.Column('pre_id', db.Integer, primary_key = True)
    pre_texto = db.Column(db.String(150))
    eva_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.eva_id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('categorias.cat_id')) 
    com_id = db.Column(db.Integer, db.ForeignKey('competencias.com_id'))
    tpr_id = db.Column(db.Integer, db.ForeignKey('tipo_preguntas.tpr_id'))

    def __init__(self, texto, categoria, tipo, competencia):
        self.pre_texto = texto
        self.cat_id = categoria
        self.com_id = competencia
        self.tpr_id = tipo


class respuesta(db.Model):
    __tablename__ = 'respuestas'

    id = db.Column('res_id', db.Integer, primary_key=True)
    res_texto = db.Column(db.String(140))
    res_valor = db.Column(db.Float)
    pre_id = db.Column(db.Integer, db.ForeignKey('preguntas.pre_id')) #Revisar

    def __init__(self, texto, valor, pregunta):
        self.res_texto = texto
        self.res_valor = valor
        self.pre_id = pregunta