from flask import Blueprint, render_template, request
from ..models import Equipo

asistente_bp = Blueprint("asistente", __name__, url_prefix="/equipos/<int:equipo_id>/asistente")

BASE_CONOCIMIENTO = [
    (["filtro", "filtros"],
     "Los filtros bacterianos/virales del circuito respiratorio deben revisarse en cada mantenimiento preventivo "
     "y cambiarse según lo indicado en el manual del fabricante (generalmente cada 15-30 días de uso continuo, "
     "o antes si se observa obstrucción o humedad excesiva)."),

    (["vaporizador", "agente anestesico", "agente anestésico"],
     "El vaporizador debe calibrarse periódicamente según el cronograma del fabricante. Verifica fugas con la "
     "prueba de presión negativa antes de cada uso, y nunca lo llenes por encima del nivel máximo indicado."),

    (["alarma", "alarmas"],
     "Si una alarma no cede, primero verifica que los parámetros configurados sean correctos para el paciente/"
     "prueba. Si persiste, revisa las conexiones de los sensores asociados y consulta el manual de servicio "
     "cargado en la sección de Manuales de este equipo antes de intervenir el equipo."),

    (["presion", "presión"],
     "Ante una alarma de presión, revisa primero posibles fugas o desconexiones en el circuito respiratorio, "
     "y confirma que el flujo de gas fresco esté dentro de rango. Documenta el hallazgo en el Checklist."),

    (["bateria", "batería"],
     "La batería de respaldo debe probarse en cada mantenimiento preventivo desconectando momentáneamente la "
     "energía eléctrica y verificando que el equipo mantenga la ventilación y monitorización sin interrupciones."),

    (["fuga", "fugas"],
     "Para detectar fugas en el circuito, realiza la prueba de hermeticidad indicada en el manual de servicio "
     "del equipo (usualmente ocluyendo la pieza en Y y verificando la caída de presión)."),

    (["calibracion", "calibración"],
     "La calibración debe realizarse con la periodicidad indicada por el fabricante o el área de metrología "
     "de la institución, y quedar documentada en la Hoja de Vida del equipo."),
]

RESPUESTA_DEFECTO = (
    "No tengo información específica sobre eso todavía. Te recomiendo revisar el manual técnico del equipo "
    "(sección Manuales) o consultar con el área de ingeniería clínica. "
    "Puedes preguntarme sobre: filtros, vaporizador, alarmas, presión, batería, fugas o calibración."
)


def buscar_respuesta(pregunta):
    pregunta_lower = pregunta.lower()
    for palabras_clave, respuesta in BASE_CONOCIMIENTO:
        if any(palabra in pregunta_lower for palabra in palabras_clave):
            return respuesta
    return RESPUESTA_DEFECTO


@asistente_bp.route("/", methods=["GET", "POST"])
def chat(equipo_id):
    equipo = Equipo.query.get_or_404(equipo_id)
    pregunta = None
    respuesta = None

    if request.method == "POST":
        pregunta = request.form.get("pregunta", "").strip()
        if pregunta:
            respuesta = buscar_respuesta(pregunta)

    return render_template("asistente/chat.html", equipo=equipo, pregunta=pregunta, respuesta=respuesta)