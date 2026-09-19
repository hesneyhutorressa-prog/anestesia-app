import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .. import db
from ..models import Equipo, Manual

manuales_bp = Blueprint("manuales", __name__, url_prefix="/equipos/<int:equipo_id>/manuales")

EXTENSIONES_PERMITIDAS = {"pdf"}


def extension_valida(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


@manuales_bp.route("/")
def listar(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    manuales = Manual.query.filter_by(equipo_id=equipo_id).all()
    return render_template("manuales/listar.html", equipo=equipo, manuales=manuales)


@manuales_bp.route("/subir", methods=["POST"])
def subir(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    archivo = request.files.get("archivo")

    if not archivo or archivo.filename == "":
        flash("No seleccionaste ningún archivo.", "error")
        return redirect(url_for("manuales.listar", equipo_id=equipo_id))

    if not extension_valida(archivo.filename):
        flash("Solo se permiten archivos PDF.", "error")
        return redirect(url_for("manuales.listar", equipo_id=equipo_id))

    nombre_original = secure_filename(archivo.filename)
    nombre_unico = f"{uuid.uuid4().hex}_{nombre_original}"
    ruta_completa = os.path.join(current_app.config["UPLOAD_FOLDER_MANUALES"], nombre_unico)
    archivo.save(ruta_completa)

    manual = Manual(
        equipo_id=equipo.id,
        nombre_archivo=nombre_original,
        ruta_archivo=f"uploads/manuales/{nombre_unico}",
        tipo=request.form.get("tipo", "manual_usuario"),
    )
    db.session.add(manual)
    db.session.commit()

    flash("Manual cargado correctamente.", "success")
    return redirect(url_for("manuales.listar", equipo_id=equipo_id))


@manuales_bp.route("/<int:manual_id>/eliminar", methods=["POST"])
def eliminar(equipo_id, manual_id):
    manual = Manual.query.get_or_404(manual_id)
    db.session.delete(manual)
    db.session.commit()
    flash("Manual eliminado.", "success")
    return redirect(url_for("manuales.listar", equipo_id=equipo_id))