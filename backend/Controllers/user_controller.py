from flask import request, jsonify
from backend.Middlewares.Mail_Sender.sender import enviar_credenciales_gmail
from backend.APIs.Bd_automat_usuarios_zeus import ConexionAutomatUsuarioZeus
from backend.APIs.Zeus.Bd_zeus import ConexionZeus
from backend.Middlewares.Hasher_md5.psw_hasher import psw_hasher
from backend.Middlewares.creds_generator.creds_generator import generate_creds
from backend.Middlewares.date_generator.date_generator import date_generator_parser

Conexion_BD=ConexionAutomatUsuarioZeus()
Conexion_Zeus = ConexionZeus()

def crear_empleado_zeus():
    retorno =Conexion_BD.comprobar_estado_funcionamiento()
    if not retorno:
        return jsonify(msg="No funcionando"),401
    peticion = request.get_json()
    cargo = peticion.get("cargo")
    nombres = [peticion.get("primer_nombre").upper(),peticion.get("segundo_nombre").upper(),
               peticion.get("primer_apellido").upper(),peticion.get("segundo_apellido").upper()]
    nombre_completo = f"{nombres[0]} {nombres[1]} {nombres[2]} {nombres[3]}"
    if nombres[1] == " ":
        nombre_completo = f"{nombres[0]} {nombres[2]} {nombres[3]}"
    numero_cedula = peticion.get("cedula_ciudadania")
    contacto = [peticion.get("telefono"),peticion.get("correo")]
    credenciales = generate_creds(nombres,numero_cedula)  
    if len(credenciales)<2:
        return jsonify(msj=f"Error en credenciales->  {credenciales}"),400
    #Retorna [fecha_actual_str, fecha_6_meses_str] en esas posiciones. O [Error]
    lista_fechas = date_generator_parser()
    if len(lista_fechas)<2:
        return jsonify(msj=lista_fechas),400
    contraseña_md5=psw_hasher(credenciales[1].strip())
    print(credenciales)
    print(contacto[0])
    try:
        Conexion_Zeus.set_beg_tran()
        msj, retorno_asistenacial=Conexion_Zeus.crear_personal_asistencial(primer_nombre=nombres[0],
                                                        segundo_nombre=nombres[1],
                                                        primer_apellido=nombres[2],
                                                        segundo_apellido=nombres[3],
                                                        nombre_completo=nombre_completo,
                                                        telefono=contacto[0],
                                                        correo=contacto[1],
                                                        documento_identidad=numero_cedula,
                                                        cargo=cargo)
        print(msj)
        msj, retorno_usuario = Conexion_Zeus.crear_usuario(nombre_completo,numero_cedula,
                                                               contacto[1],credenciales[0].strip(),credenciales[1].strip(),
                                                               contraseña_md5,cargo)
        print(msj)
        if not all([retorno_usuario,retorno_asistenacial]):
            return jsonify(mjg="Error en las Creacion y Habilitacin Usuario"),418
        Conexion_Zeus.set_beg_tran()
        if cargo !="AUXILIAR ENFERMERIA" or cargo!="CUIDADOR":
            msj,retorno_habilitar_programacion = Conexion_Zeus.habilitar_programacion(nombre_completo)
            print(msj)
            msj, retorno_habilitar_agenda = Conexion_Zeus.habilitar_agenda(nombre_completo,lista_fechas[0],lista_fechas[1],cargo)
            print(msj)
        msj, retorno_punto_atencion = Conexion_Zeus.asignar_punto_atencion(numero_cedula)
        print(msj)
        if not all([retorno_habilitar_agenda and retorno_punto_atencion and retorno_habilitar_programacion]):
            return jsonify(msg= "Error en Agenda y/o PuntoAtencion"),418
        msj, retorno= enviar_credenciales_gmail(contacto[1],credenciales[0],credenciales[1],cargo,nombre_completo)
        if not retorno:
            return jsonify(msg=msj),400
        Conexion_BD.registrar_empleado_creado(nombres[0],nombres[1],nombres[2],nombres[3],nombre_completo,
                                              contacto[1],contacto[0],numero_cedula,cargo,credenciales[0].strip(),contraseña_md5,credenciales[1])
        
        return jsonify(msj = "Usuario creado con exito", retorno=True),200
    except Exception as e:
        return jsonify(msg=f"Error-> {e}" , retorno=False),400

    