import pymssql
from backend.Middlewares.SaaS.SaaS import saas
import functools

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
        
    @staticmethod
    def wrapper_reconect(func):
        """Decorador para reconectar si la conexión está caída."""
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            saas()
            try:
                # Intenta ejecutar una consulta simple para verificar conexión
                with self.conexion.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except pymssql.Error:
                # Reconectar si hay error
                print("Conexión perdida. Reconectando...")
                self.conexion = pymssql.connect(**self._config)
                print("Reconectado exitosamente.")
            return func(self, *args, **kwargs)
        return wrapped

            
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

    @wrapper_reconect
    def habilitar_programacion(self,nombre_completo):
        '''Retorna Array [MSJ] y Boolean'''
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("Exec spProgramaciones @Op='Guardar',@Nombre=%s,@Activo='1'",(nombre_completo,))
                return ["Habilitacion en programacion Exitosa"], True
        except:
            return ["Error en la habilitacion de Programacion"], False
        finally:
            self.conexion.close()
            cursor.close()

    @wrapper_reconect
    def habilitar_agenda(self,nombre_completo,fecha_inicio,fecha_fin):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("select id from programacion where Nombre = %s",(nombre_completo,))
                programacion_id= cursor.fetchall()[0][0]
                if not programacion_id:
                    return ["No se encontró programacion ID"], False
                cursor.execute("""Exec spInsertarProgramacionMedico 
                               @fechainicio='2025/07/11',@fechafin='2025/07/16',@horainicio='04:00',@meridianoi='am',@horafinal='11:00',@meridianof='pm',
                               @intervalo=30,@id_programacion=720,@op='agregarProgramacion'
                               ,@id_sede=1,@nro_paciente=0,@lun=1,@mar=1,@mie=1,@jue=1,@vie=1,@sab=1,@dom=1,
                               @txtLun='',@txtMar='',@txtMie='',@txtJue='',@txtVie='',@txtSab='',@txtDom='',@IdFestivos='',@CalcularIntervalo=0""")
                return ["asignacion fecha exitosa"], True
        except Exception as e:
            return ["Error en la asignacion de fehca"], False
        finally:
            self.conexion.close()
            cursor.close()

    def crear_personal_asistencial_auxiliar_cuidadora(self,peticion):
    
        pass

    @wrapper_reconect
    def crear_personal_asistencial_antibiotico(self,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,
                                               nombre_completo,telefono,correo,documento_identidad):
        '''Retorna Array [Mensaje] y Boolean'''
        especialidad =self.especialidades.get("ANTIBIOTICOTERAPIA")
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT TOP 1 COUNT(*) FROM sis_medi WHERE cedula = '12312'")
            if cursor.fetchall():
                return ["Personal asistencial con cedula ya existente"], False
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
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT TOP 1 COUNT(*) FROM usuario WHERE usuario = %s OR cedula = %s",(usuario,documento_identidad))
                if cursor.fetchall:
                    return ["Usuario ya existente"],False
                cursor.execute("""INSERT INTO usuario 
		    		            (usuario, cedula, nombre,
                                nivel, status,
                                email, codigo,
                                fecha, nivel_externo, bodega, inf_pedido,autoriza,
                               pass,
                               Solicitante,cierra_sesion_users, AnulaRecibos,anulaRHC,intercalarHC,LQ_DctosNoRestriccion,GeneraReciboCaja, ModificaMovContableFacts,AuditaFE,IdComputadorAsignado,SerialComputador,FirmaBase64)
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
                return [],True
        except Exception as e:
            return [] ,False


    def crear_personal_asistencial_auxiliar_cuidadora(self):
        pass

    