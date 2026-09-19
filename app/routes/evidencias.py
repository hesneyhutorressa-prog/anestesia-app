import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, redirect, url_for, flash, current_app
from .. import db
from ..models import Historial, Evidencia

evidencias_bp = Blueprint("evidencias", __name__, url_prefix="/equipos/<int:equipo_id>/historial/<int:historial_id>/evidencias")

EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "webp"}


def extension_valida(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


@evidencias_bp.route("/subir", methods=["POST"])
def subir(equipo_id, historial_id):
    registro = Historial.query.get_or_404(historial_id)
    archivo = request.files.get("foto")

    if not archivo or archivo.filename == "":
        flash("No seleccionaste ninguna foto.", "error")
        return redirect(url_for("historial.detalle", equipo_id=equipo_id, historial_id=historial_id))

    if not extension_valida(archivo.filename):
        flash("Formato no permitido. Usa PNG, JPG o WEBP.", "error")
        return redirect(url_for("historial.detalle", equipo_id=equipo_id, historial_id=historial_id))

    nombre_seguro = secure_filename(archivo.filename)
    nombre_unico = f"{uuid.uuid4().hex}_{nombre_seguro}"
    ruta_completa = os.path.join(current_app.config["UPLOAD_FOLDER_EVIDENCIAS"], nombre_unico)
    archivo.save(ruta_completa)

    evidencia = Evidencia(
        historial_id=registro.id,
        ruta_archivo=f"uploads/evidencias/{nombre_unico}",
        descripcion=request.form.get("descripcion", ""),
    )
    db.session.add(evidencia)
    db.session.commit()

    flash("Evidencia fotográfica agregada.", "success")
    return redirect(url_for("historial.detalle", equipo_id=equipo_id, historial_id=historial_id))


@evidencias_bp.route("/<int:evidencia_id>/eliminar", methods=["POST"])
def eliminar(equipo_id, historial_id, evidencia_id):
    evidencia = Evidencia.query.get_or_404(evidencia_id)
    db.session.delete(evidencia)
    db.session.commit()
    flash("Evidencia eliminada.", "success")
    return redirect(url_for("historial.detalle", equipo_id=equipo_id, historial_id=historial_id))