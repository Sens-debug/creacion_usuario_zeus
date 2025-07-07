from flask import request, jsonify
from backend.APIs.Bd_automat_usuarios_zeus import ConexionAutomatUsuarioZeus
from backend.APIs.Bd_zeus import ConexionZeus
from backend.Middlewares.Hasher_md5.psw_hasher import psw_hasher

Conexion_BD=ConexionAutomatUsuarioZeus()
Conexion_Zeus = ConexionZeus()

def crear_empleado_zeus_antibiotico():
    peticion = request.get_json()
    retorno =Conexion_BD.comprobar_estado_funcionamiento()
    if not retorno:
        return jsonify(msg="No funcionando"),401
    nombres = [peticion.get("primer_nombre"),peticion.get("segundo_nombre"),
               peticion.get("primer_apellido"),peticion.get("segundo_apellido")]
    nombre_completo = f"{nombres[0]} {nombres[1]} {nombres[2]} {nombres[3]}"
    numero_cedula = peticion.get("cedula_ciudadania")
    contacto = [peticion.get("telefono"),peticion.get("correo")]
    credenciales = [peticion.get("usuario"),peticion.get("contraseña")]
    contraseña_md5=psw_hasher(credenciales[1])
    try:
        msj, retorno=Conexion_Zeus.crear_personal_asistencial_antibiotico(primer_nombre=nombres[0],
                                                        segundo_nombre=nombres[1],
                                                        primer_apellido=nombres[2],
                                                        segundo_apellido=nombres[3],
                                                        nombre_completo=nombre_completo,
                                                        telefono=contacto[0],
                                                        correo=contacto[1],
                                                        documento_identidad=numero_cedula)
        if not retorno:
            return jsonify(msg=msj),401
        msj, retorno = Conexion_Zeus.crear_usuario_antibiotico(nombre_completo,numero_cedula,
                                                               contacto[1],credenciales[0],credenciales[1],
                                                               contraseña_md5)
        if not retorno:
            return jsonify(msg=msj),401
        
        
    except Exception as e:
        return jsonify(msg="Error-> "+e , retorno=False),400

    pass