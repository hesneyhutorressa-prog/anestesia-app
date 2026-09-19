import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Equipo, Checklist, Historial

checklist_bp = Blueprint("checklist", __name__, url_prefix="/equipos/<int:equipo_id>/checklist")

ITEMS_PREVENTIVO = [
    "Suministro de gases medicinales (O2, N2O, Aire)",
    "Sistema de dosificación (flujómetros)",
    "Vaporizador de agente anestésico",
    "Circuito respiratorio del paciente",
    "Ventilador mecánico integrado",
    "Sistema de evacuación de gases (AGSS)",
    "Módulo de monitorización (SpO2, CO2, Presión)",
    "Alarmas y unidad de control electrónico",
    "Interfaz de usuario (pantalla táctil)",
    "Limpieza general y estado físico del equipo",
]


@checklist_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)

    if request.method == "POST":
        tipo = request.form.get("tipo")
        tecnico = request.form.get("tecnico")
        marcados = request.form.getlist("items")
        descripcion_extra = request.form.get("descripcion", "")

        checklist = Checklist(
            equipo_id=equipo.id,
            tipo=tipo,
            tecnico=tecnico,
            estado="completado",
            items_json=json.dumps(marcados),
        )
        db.session.add(checklist)
        db.session.flush()

        resumen = f"{len(marcados)}/{len(ITEMS_PREVENTIVO)} ítems verificados."
        if descripcion_extra:
            resumen += f" Observaciones: {descripcion_extra}"

        historial = Historial(
            equipo_id=equipo.id,
            checklist_id=checklist.id,
            fecha=datetime.utcnow(),
            descripcion=resumen,
            tecnico=tecnico,
        )
        db.session.add(historial)
        db.session.commit()

        flash("Checklist registrado y agregado al historial.", "success")
        return redirect(url_for("historial.listar", equipo_id=equipo.id))

    return render_template("checklist/nuevo.html", equipo=equipo, items=ITEMS_PREVENTIVO)