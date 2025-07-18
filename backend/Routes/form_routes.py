from flask import Blueprint
from backend.Controllers.user_controller import crear_empleado_zeus


user_bp = Blueprint('form',__name__)

#Ruta login
user_bp.route('/crear_usuario', methods=['POST'])(crear_empleado_zeus)
