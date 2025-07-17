from flask import Blueprint
from backend.Controllers.user_controllers.user_antibiotic_controller import crear_empleado_zeus_antibiotico
from backend.Controllers.user_controllers.user_caregiver_controller import crear_empleado_zeus_cuidadora
from backend.Controllers.user_controllers.user_nurse_controller import crear_empleado_zeus_auxiliar

user_bp = Blueprint('form',__name__)

#Ruta login
user_bp.route('/crear_antibiotico', methods=['POST'])(crear_empleado_zeus_antibiotico)
user_bp.route('/crear_cuidadora', methods=['POST'])(crear_empleado_zeus_cuidadora)
user_bp.route('/crear_auxiliar', methods = ['POST'])(crear_empleado_zeus_auxiliar)