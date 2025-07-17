from flask import Blueprint
from backend.Controllers.form_controller import crear_empleado_zeus_antibiotico

form_bp = Blueprint('form',__name__)

#Ruta login
form_bp.route('/crear_usuario', methods=['POST'])(crear_empleado_zeus_antibiotico)