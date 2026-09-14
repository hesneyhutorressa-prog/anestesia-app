import os
import qrcode
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from .. import db
from ..models import Equipo

equipos_bp = Blueprint("equipos", __name__, url_prefix="/equipos")


@equipos_bp.route("/")
def listar():
    equipos = Equipo.query.order_by(Equipo.fecha_registro.desc()).all()
    return render_template("equipos/listar.html", equipos=equipos)


@equipos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        codigo = request.form["codigo_interno"].strip().upper()

        if Equipo.query.filter_by(codigo_interno=codigo).first():
            flash(f"Ya existe un equipo con el código {codigo}.", "error")
            return redirect(url_for("equipos.nuevo"))

        equipo = Equipo(
            codigo_interno=codigo,
            nombre=request.form["nombre"],
            marca=request.form.get("marca"),
            modelo=request.form.get("modelo"),
            numero_serie=request.form.get("numero_serie"),
            ubicacion=request.form.get("ubicacion"),
            estado="Operativo",
        )
        db.session.add(equipo)
        db.session.commit()

        qr_url = url_for("equipos.pantalla_principal", equipo_id=equipo.id, _external=True)
        qr_img = qrcode.make(qr_url)
        qr_filename = f"equipo_{equipo.id}.png"
        qr_full_path = os.path.join(current_app.config["QR_FOLDER"], qr_filename)
        qr_img.save(qr_full_path)

        equipo.qr_path = f"qrcodes/{qr_filename}"
        db.session.commit()

        flash(f"Equipo {codigo} registrado y QR generado correctamente.", "success")
        return redirect(url_for("equipos.ver_qr", equipo_id=equipo.id))

    return render_template("equipos/nuevo.html")


@equipos_bp.route("/<int:equipo_id>/qr")
def ver_qr(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    return render_template("equipos/ver_qr.html", equipo=equipo)


@equipos_bp.route("/<int:equipo_id>")
def pantalla_principal(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    return render_template("equipos/pantalla_principal.html", equipo=equipo)