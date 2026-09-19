import json
from flask import Blueprint, render_template
from ..models import Equipo, Historial

historial_bp = Blueprint("historial", __name__, url_prefix="/equipos/<int:equipo_id>/historial")


@historial_bp.route("/")
def listar(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    registros = Historial.query.filter_by(equipo_id=equipo_id).order_by(Historial.fecha.desc()).all()
    return render_template("historial/listar.html", equipo=equipo, registros=registros)


@historial_bp.route("/<int:historial_id>")
def detalle(equipo_id, historial_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    registro = Historial.query.get_or_404(historial_id)
    items = json.loads(registro.checklist.items_json) if registro.checklist else []
    return render_template("historial/detalle.html", equipo=equipo, registro=registro, items=items)