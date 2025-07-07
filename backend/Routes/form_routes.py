from flask import Blueprint
from backend.Controllers.auth_controller import login

auth_bp = Blueprint('form',__name__)

#Ruta login
auth_bp.route('/crear_usuario', methods=['POST'])(login)