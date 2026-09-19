from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Equipo, Inventario

inventario_bp = Blueprint("inventario", __name__, url_prefix="/equipos/<int:equipo_id>/inventario")


@inventario_bp.route("/")
def listar(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    items = Inventario.query.filter_by(equipo_id=equipo_id).all()
    return render_template("inventario/listar.html", equipo=equipo, items=items)


@inventario_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)

    if request.method == "POST":
        item = Inventario(
            equipo_id=equipo.id,
            repuesto=request.form["repuesto"],
            cantidad=int(request.form.get("cantidad") or 0),
            stock_minimo=int(request.form.get("stock_minimo") or 1),
            ubicacion_bodega=request.form.get("ubicacion_bodega"),
        )
        db.session.add(item)
        db.session.commit()
        flash("Repuesto agregado al inventario.", "success")
        return redirect(url_for("inventario.listar", equipo_id=equipo.id))

    return render_template("inventario/nuevo.html", equipo=equipo)


@inventario_bp.route("/<int:item_id>/eliminar", methods=["POST"])
def eliminar(equipo_id, item_id):
    item = Inventario.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Repuesto eliminado.", "success")
    return redirect(url_for("inventario.listar", equipo_id=equipo_id))