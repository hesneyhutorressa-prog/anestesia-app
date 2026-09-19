from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Equipo, HojaDeVida

hoja_vida_bp = Blueprint("hoja_vida", __name__, url_prefix="/equipos/<int:equipo_id>/hoja-vida")


@hoja_vida_bp.route("/", methods=["GET", "POST"])
def ver(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)

    if request.method == "POST":
        fecha_str = request.form.get("fecha_adquisicion")
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else None

        if equipo.hoja_vida:
            hv = equipo.hoja_vida
        else:
            hv = HojaDeVida(equipo_id=equipo.id)
            db.session.add(hv)

        hv.fecha_adquisicion = fecha
        hv.proveedor = request.form.get("proveedor")
        hv.vida_util_anios = request.form.get("vida_util_anios") or None
        hv.responsable = request.form.get("responsable")

        db.session.commit()
        flash("Hoja de vida guardada correctamente.", "success")
        return redirect(url_for("hoja_vida.ver", equipo_id=equipo.id))

    return render_template("hoja_vida/ver.html", equipo=equipo, hv=equipo.hoja_vida)