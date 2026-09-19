from flask import Blueprint, render_template
from ..models import Equipo, Historial, Inventario

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def index():
    total_equipos = Equipo.query.count()
    operativos = Equipo.query.filter_by(estado="Operativo").count()
    en_mantenimiento = Equipo.query.filter(Equipo.estado != "Operativo").count()

    ultimos_mantenimientos = (
        Historial.query.order_by(Historial.fecha.desc()).limit(5).all()
    )

    alertas_inventario = (
        Inventario.query.filter(Inventario.cantidad <= Inventario.stock_minimo).all()
    )

    return render_template(
        "dashboard/index.html",
        total_equipos=total_equipos,
        operativos=operativos,
        en_mantenimiento=en_mantenimiento,
        ultimos_mantenimientos=ultimos_mantenimientos,
        alertas_inventario=alertas_inventario,
    )