from datetime import datetime
from . import db


class Equipo(db.Model):
    __tablename__ = "equipos"

    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))
    ubicacion = db.Column(db.String(150))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default="Operativo")
    qr_path = db.Column(db.String(255))

    hoja_vida = db.relationship("HojaDeVida", backref="equipo", uselist=False, cascade="all, delete-orphan")
    inventario = db.relationship("Inventario", backref="equipo", cascade="all, delete-orphan")
    checklists = db.relationship("Checklist", backref="equipo", cascade="all, delete-orphan")
    historial = db.relationship("Historial", backref="equipo", cascade="all, delete-orphan")
    manuales = db.relationship("Manual", backref="equipo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Equipo {self.codigo_interno} - {self.nombre}>"


class HojaDeVida(db.Model):
    __tablename__ = "hoja_de_vida"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    fecha_adquisicion = db.Column(db.Date)
    proveedor = db.Column(db.String(150))
    vida_util_anios = db.Column(db.Integer)
    responsable = db.Column(db.String(150))


class Inventario(db.Model):
    __tablename__ = "inventario"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    repuesto = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=1)
    ubicacion_bodega = db.Column(db.String(100))


class Checklist(db.Model):
    __tablename__ = "checklist"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.String(20))
    tecnico = db.Column(db.String(150))
    estado = db.Column(db.String(20), default="completado")
    items_json = db.Column(db.Text)

    historial = db.relationship("Historial", backref="checklist", uselist=False)


class Historial(db.Model):
    __tablename__ = "historial"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    checklist_id = db.Column(db.Integer, db.ForeignKey("checklist.id"))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text)
    tecnico = db.Column(db.String(150))

    evidencias = db.relationship("Evidencia", backref="historial", cascade="all, delete-orphan")


class Evidencia(db.Model):
    __tablename__ = "evidencias"

    id = db.Column(db.Integer, primary_key=True)
    historial_id = db.Column(db.Integer, db.ForeignKey("historial.id"), nullable=False)
    ruta_archivo = db.Column(db.String(255), nullable=False)
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(255))


class Manual(db.Model):
    __tablename__ = "manuales"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    nombre_archivo = db.Column(db.String(255))
    ruta_archivo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50))