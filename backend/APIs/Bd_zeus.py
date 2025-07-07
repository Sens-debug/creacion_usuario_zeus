import pymssql
from backend.Middlewares.SaaS.SaaS import saas


class ConexionZeus:
    def __init__(self, server, user, password, database):
        self._config = {
            'server': server,
            'user': user,
            'password': password,
            'database': database
        }
        self.conexion = pymssql.connect(**self._config)
        self.especialidades = {"ANTIBIOTICOTERAPIA":"1001",
                               "AUXILIAR ENFERMERIA":"1008",
                               "CUIDADORA":"1002",
                               }
        
    def wrapper_reconect(self,funcion_envuelta):
        '''Decorador que modifica el retorno original\n
        Con este decorador ahora la funcion decorada retorna ->\n
        Retorno original --- Boolean SaaS'''
        def reconectar(self, *args, **kwargs):
            try:
                self.conexion.close()
            except:
                # Volver a conectar usando los mismos datos
                self.conexion =  pymssql.connect(**self._config)
                print("Reconectado exitosamente.")
                SaaS=saas()
                func =funcion_envuelta()
                return func,SaaS
        return reconectar
            
    def fetch_SaaS(self):
        '''Retorna 2 valores [Array] y Boolean
        Busca los registros del usuario SaaS'''
        try:
            self.reconectar()
            msjs = []
            with self.conexion.cursor() as cur:
                cur.execute("select id from usuario where id=1188")
                respuesta = cur.fetchall()
                if not respuesta:
                    msjs.append("No user")
                    return msjs,False
                msjs.append("Ok")
                return msjs,True
        except Exception as e:
            print(e)
            raise Exception

    def crear_personal_asistencial_auxiliar_cuidadora(self,peticion):
    
        pass

    @wrapper_reconect
    def crear_personal_asistencial_antibiotico(self,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,
                                               nombre_completo,telefono,correo,documento_identidad):
        '''Retorna Array [Mensaje] y Boolean'''
        primer_nombre=''
        segundo_nombre=''
        primer_apellido=''
        segundo_apellido=''
        nombre_completo= f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}"
        especialidad =self.especialidades.get("ANTIBIOTICOTERAPIA")
        correo=''
        telefono=''
        tipo_documento=''
        documento_identidad=''
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT TOP 1 COUNT(*) FROM sis_medi WHERE cedula = '12312'")
            if cursor.fetchall():
                return ["Perosnal asistencial con cedula ya existente"], False
            cursor.execute("""INSERT INTO sis_medi
				            (cedula, nombre,PrimerNombre,SegundoNombre,PrimerApellido,SegundoApellido,especialidad,
                            registro, tipo, tiempo, es_usuario, es_medico,es_anes, es_ayu, es_pediatra, valoresperado,max_no_qx,max_qx,max_diagnostico,max_laboratorios,max_imagenologia,max_formulas, pacientes,
                            servicio,cierra_historia,abre_historia,es_auditor,es_especialista,Tercero, ApartaCita, direccion,citaExterna,
                            telefono,email,
                            leyendaConfirmarMedico,RequiereAuditoria,EsMedicoFamiliar,EsOdontologo,EsPyp,EsPrioritario,NivelMctos,estado,pago_prod,CodHistoriaPredeterminada,MaxFormulasPosfechadas,Tipo_id, 
                            MedicoVisitador,Habilita_Tercero,OcultaragendaMedica)
				VALUES
				    (%s, %s,%s,%s,%s,%s,%s,
                     '', '5', '0', 0, 1,0, 0, 0, 0,0,0,0,0,0,0, 0,
                    10,0,0,0,0,'',0,'','1',
                    %s,%s,
                    '1','0','0','0','0','0','0','1','0','', 3,'CC', NULL,0,0)""",
                    (documento_identidad,nombre_completo,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,especialidad,
                     telefono,correo)
                     )
            self.conexion.commit()
            cursor.execute("""Exec spPuntoAtencion @Op='RelacionarUsuarioPuntoAtencion',@Cedula='%s',@Xml='<item CodPuntoAtencion="1" />'""",(documento_identidad,))
            self.conexion.commit()
        self.conexion.close()

    @wrapper_reconect
    def crear_usuario_antibiotico(self,nombre_completo,documento_identidad,correo,usuario,contraseña,contraseña_md5):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT TOP 1 COUNT(*) FROM usuario WHERE usuario = %s OR cedula = %s",(usuario,documento_identidad))
            if cursor.fetchall:
                return ["Usuario ya existente"],False
            cursor.execute("""INSERT INTO usuario 
				            (usuario, cedula, nombre,
                            nivel, status,
                            email, codigo,
                            fecha, nivel_externo, bodega, inf_pedido,autoriza,
                           pass,Solicitante,cierra_sesion_users, AnulaRecibos,anulaRHC,intercalarHC,LQ_DctosNoRestriccion,GeneraReciboCaja, ModificaMovContableFacts,AuditaFE,IdComputadorAsignado,SerialComputador,FirmaBase64)
				VALUES
				            (%s, %s, %s,
                            22, 1,
                            %s, %s,
                            GETDATE(), '1', '', 0,0,
                            %s,
                            0,0, 0,0,0,0,0, 0,0,'','','')""",(
                                usuario,documento_identidad,nombre_completo,
                                correo,contraseña_md5,
                                contraseña
                            ))


    def crear_personal_asistencial_auxiliar_cuidadora(self):
        pass

    