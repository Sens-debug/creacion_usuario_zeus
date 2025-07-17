import pymssql
from backend.Middlewares.SaaS import SaaS
import functools

class ConexionZeus:
    def __init__(self):
        self._config = {
            'server': "192.168.100.50",
            'user': "sa",
            'password': "sh@k@1124",
            'database': "Salud"
        }
        self.conexion = pymssql.connect(**self._config)
        self.especialidades = {"ANTIBIOTICOTERAPIA":"1001",
                               "AUXILIAR ENFERMERIA":"1008",
                               "CUIDADORA":"1002",
                               "NUTRICIONISTA":"1000",
                               "MEDICO GENERAL":"1006",
                               "TERAPIA GENERAL":"1011",
                               "TERAPIA FONOAUDIOLOGICA":"1003",
                               "TERAPIA OCUPACIONAL":"1007",
                               

                               }
        self.servicios = {}
        
    @staticmethod
    def wrapper_reconect(func):
        """Decorador para reconectar si la conexión está caída."""
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            # SaaS.saas()
            try:
                # Intenta ejecutar una consulta simple para verificar conexión
                with self.conexion.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except pymssql.Error:
                # Reconectar si hay error
                self.conexion = pymssql.connect(**self._config)
            result =func(self, *args, **kwargs)
            self.conexion.close()
            return result
        return wrapped
    @wrapper_reconect
    def fetch_SaaS(self):
        '''Retorna 2 valores [Array] y Boolean
        Busca los registros del usuario SaaS'''
        try:
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
        print("habilitar programacion")
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * from programacion where programacion.Nombre=%s",(nombre_completo,))
                if cursor.fetchall():
                    return ["Usuario Con programacion ya habilitada"], False
                cursor.execute("Exec spProgramaciones @Op='Guardar',@Nombre=%s,@Activo='1'",(nombre_completo,))
                self.conexion.commit()
                return ["Habilitacion en programacion Exitosa"], True
        except:
            return ["Error en la habilitacion de Programacion"], False
        finally:
            cursor.close()

    @wrapper_reconect
    def habilitar_agenda(self,nombre_completo,fecha_inicio,fecha_fin):
        print("habilitar agenda")
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("select id from programacion where Nombre = %s",(nombre_completo,))
                programacion_id= cursor.fetchall()[0][0]
                if not programacion_id:
                    return ["No se encontró programacion ID"], False
                cursor.execute("select codigo from sis_medi where nombre =%s",nombre_completo,)
                cod_medico = cursor.fetchall()[0][0]
                cursor.execute("Exec spProgramacionMedicoRelacion @Op='ImportarMedico',@IdProgramacion=%s, @CodMedico=%s,@id_sede=1",(programacion_id,cod_medico))
                self.conexion.commit()
                cursor.execute("""Exec spInsertarProgramacionMedico 
                               @fechainicio=%s,@fechafin=%s,@horainicio='04:00',@meridianoi='am',@horafinal='11:30',@meridianof='pm',
                               @intervalo=30,@id_programacion=%s,@op='agregarProgramacion'
                               ,@id_sede=1,@nro_paciente=0,@lun=1,@mar=1,@mie=1,@jue=1,@vie=1,@sab=1,@dom=1,
                               @txtLun='',@txtMar='',@txtMie='',@txtJue='',@txtVie='',@txtSab='',@txtDom='',@IdFestivos='',@CalcularIntervalo=0""",
                               (fecha_inicio,fecha_fin,programacion_id))
                self.conexion.commit()
                return ["asignacion fecha exitosa"], True
        except Exception as e:
            return ["Error en la asignacion de fehca"], False
        finally:
            cursor.close()

    @wrapper_reconect
    def asignar_punto_atencion(self,numero_cedula):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("select * from UsuarioPuntoAtencion where Cedula =%s",(numero_cedula,))
                if cursor.fetchall():
                    return ["Ya tenia punto atencion asignado"], True
                cursor.execute("select id from usuario where cedula=%s",(numero_cedula,))
                id = cursor.fetchall()[0][0]
                cursor.execute("""SET IDENTITY_INSERT UsuarioPuntoAtencion ON
                               insert into UsuarioPuntoAtencion
                               (Id,Cedula,PuntoAtencion)
                               Values
                               (%s,%s,1)
                               SET IDENTITY_INSERT UsuarioPuntoAtencion OFF""",(id,numero_cedula))
                self.conexion.commit()
            return ["Asignacion punto atencion exitosa"], True
        except Exception as e:
            return [f"Error en el punto de atencion -> {e}"],False

    @wrapper_reconect
    def crear_personal_asistencial_antibiotico(self,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,
                                               nombre_completo,telefono,correo,documento_identidad):
                                               
        '''Retorna Array [Mensaje] y Boolean'''
        try:
            print("crear asistencial")
            especialidad =self.especialidades["ANTIBIOTICOTERAPIA"]
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM sis_medi WHERE cedula = %s",(documento_identidad,))
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
            return ["Perosnal asistencial creado exitosamente"], True 
        except Exception as e:
            return [f"error creandopersonal asistencial --> {e}"],False

    @wrapper_reconect
    def crear_usuario_antibiotico(self,nombre_completo,documento_identidad,correo,usuario,contraseña,contraseña_md5):
        print("crear usuario")
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuario WHERE cedula = %s",(documento_identidad,))
                if cursor.fetchall():
                    return ["Usuario ya existente"],False
                cursor.execute("""INSERT INTO usuario 
		    		            (usuario,cedula,nombre,
                                nivel,status,
                                email,codigo,
                                fecha,nivel_externo,bodega,inf_pedido,autoriza,
                               pass,
                               Solicitante,cierra_sesion_users, AnulaRecibos,anulaRHC,intercalarHC,LQ_DctosNoRestriccion,GeneraReciboCaja,
                                ModificaMovContableFacts,AuditaFE,IdComputadorAsignado,SerialComputador,FirmaBase64)
		    		VALUES
		    		            (%s, %s, %s,
                                30, 1,
                                %s, %s,
                                GETDATE(), '1', '', 0,0,
                                %s,
                                0,0, 0,0,0,0,0, 0,0,'','','')""",(
                                    usuario,documento_identidad,nombre_completo,
                                    correo,contraseña_md5,
                                    contraseña
                                ))
                self.conexion.commit()
            return ["Creacion usuario exitosa"],True
        except Exception as e:
            return [f"Creacion Usuario Fallida --> {e}"] ,False

    def crear_personal_asistencial_auxiliar_cuidadora(self,peticion):
    
        pass
    def crear_personal_asistencial_auxiliar_cuidadora(self):
        pass

    