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
                               "CUIDADOR":"1002",
                               "NUTRICION":"1000",
                               "MEDICINA GENERAL":"1006",
                               "MEDICINA GENERAL MEDIO TIEMPO":"1006",
                               "TERAPIA GENERAL":"1011",
                                "TERAPIA FONOAUDIOLOGICA":"1003",
                                "TERAPIA OCUPACIONAL":"1007",
                                "TERAPIA FISICA":"1",
                                "TERAPIA RESPIRATORIA":"1004",
                               "PSICOLOGIA":"1005"
                               }
        self.servicios = {"ANTIBIOTICOTERAPIA":"10",
                          "CUIDADOR":"4",
                          "AUXILIAR ENFERMERIA":"4",
                          "NUTRICION":"6",
                          "TERAPIA FISICA":"9",
                          "TERAPIA OCUPACIONAL":"8",
                          "TERAPIA FONOAUDIOLOGICA":"3",
                          "TERAPIA GENERAL":"16",
                          "TERAPIA RESPIRATORIA":"1",
                          "MEDICINA GENERAL":"2",
                          "MEDICINA GENERAL MEDIO TIEMPO":"2"
                        }
        self.niveles_acceso={"ANTIBIOTICOTERAPIA":"30",
                             "AUXILIAR ENFERMERIA":"29",
                             "CUIDADOR":"29",
                             "NUTRICION":"6",
                             "TERAPIA FONOAUDIOLOGICA":"5",
                             "TERAPIA RESPIRATORIA":"4",
                             "TERAPIA OCUPACIONAL":"2",
                             "TERAPIA FISICA":"3",
                             "TERAPIA GENERAL":"3",
                             "PSICOLOGIA":"7",
                             "MEDICINA GENERAL MEDIO TIEMPO":"1",
                             "MEDICINA GENERAL":"1"}
        
        self.tipos = {"ANTIBIOTICOTERAPIA":"5",
                      "CUIDADOR":"4",
                      "AUXILIAR ENFERMERIA":"4",
                      "TERAPIA FISICA":"6",
                      "TERAPIA OCUPACIONAL":"6",
                      "TERAPIA FONOAUDIOLOGICA":"6",
                      "TERAPIA GENERAL":"6",
                      "TERAPIA RESPIRATORIA":"6",
                      "MEDICINA GENERAL":"2",
                      "MEDICINA GENERAL MEDIO TIEMPO":"2",
                      "PSICOLOGIA":"5",
                      "NUTRICION":"5"}
        
        self.horas_habilitadas = {"ANTIBIOTICOTERAPIA":{"horas":{"inicio":"4:00",
                                                                 "fin":"11:30"},
                                                        "meridianos":{"inicio":"am",
                                                                      "fin":"pm"},
                                                        "intervalo":"40"
                                                        },
                                  "MEDICINA GENERAL":{"horas":{"inicio":"7:00",
                                                             "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                  "fin":"pm"},
                                                    "intervalo":"60"
                                                    },
                                  "MEDICINA GENERAL MEDIO TIEMPO":{"horas":{"inicio":"7:00",
                                                                        "fin":"12:00"},
                                                                "meridianos":{"inicio":"am",
                                                                              "fin":"pm"},
                                                                "intervalo":"60"
                                                                },
                                  "TERAPIA FISICA":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "TERAPIA OCUPACIONAL":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "TERAPIA FONOAUDIOLOGICA":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "TERAPIA GENERAL":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "TERAPIA RESPIRATORIA":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "NUTRICION":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   },
                                  "PSICOLOGIA":{"horas":{"inicio":"7:00",
                                                            "fin":"7:00"},
                                                    "meridianos":{"inicio":"am",
                                                                "fin":"pm"},
                                                    "intervalo":"60"
                                                   }
                                }
        
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
    
    def close_conexion(self):
        self.conexion.close()
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
    def set_rollback(self):
        print("rollback")
        self.conexion.rollback()
    @wrapper_reconect
    def set_commit(self):
        for i in range (1,20):
            self.conexion.commit()
    @wrapper_reconect
    def set_beg_tran(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("begin tran")
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
        except Exception as e:
            return [f"Error en la habilitacion de Programacion--> {e}"], False
        finally:
            cursor.close()
    @wrapper_reconect
    def habilitar_agenda(self,nombre_completo,fecha_inicio,fecha_fin,cargo):
        print("habilitar agenda")
        try:
            json_cargo= self.horas_habilitadas[cargo]
            print(json_cargo)
            json_horas=json_cargo["horas"]
            print(json_horas)
            json_meridianos=json_cargo["meridianos"]
            print(json_meridianos)
            print(fecha_inicio,fecha_fin,json_horas["inicio"],json_meridianos["inicio"],
                                json_horas["fin"],json_meridianos["fin"],
                                json_cargo["intervalo"])
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
                               @fechainicio=%s,@fechafin=%s,@horainicio=%s,@meridianoi=%s,
                               @horafinal=%s,@meridianof=%s,
                               @intervalo=%s,@id_programacion=%s,@op='agregarProgramacion'
                               ,@id_sede=1,@nro_paciente=0,@lun=1,@mar=1,@mie=1,@jue=1,@vie=1,@sab=1,@dom=1,
                               @txtLun='',@txtMar='',@txtMie='',@txtJue='',@txtVie='',@txtSab='',@txtDom='',@IdFestivos='',@CalcularIntervalo=0""",
                               (fecha_inicio,fecha_fin,json_horas["inicio"],json_meridianos["inicio"],
                                json_horas["fin"],json_meridianos["fin"],
                                json_cargo["intervalo"],
                                programacion_id))
                self.conexion.commit()
                return ["asignacion fecha exitosa"], True
        except Exception as e:
            return [f"Error en la asignacion de fechas---> {e}"], False
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
#----------------------------------------------------------------------
    @wrapper_reconect
    def crear_personal_asistencial(self,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,
                                               nombre_completo,telefono,correo,documento_identidad,cargo):
                                               
        '''Retorna Array [Mensaje] y Boolean'''
        try:
            print("crear asistencial")
            especialidad =self.especialidades[cargo]
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
                         '', %s, '0', 0, 1,0, 0, 0, 0,0,0,0,0,0,0, 0,
                        %s,0,0,0,0,'',0,'','1',
                        %s,%s,
                        '1','0','0','0','0','0','0','1','0','', 3,'CC', NULL,0,0)""",
                        (documento_identidad,nombre_completo,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,especialidad,
                         self.tipos[cargo],self.servicios[cargo],
                         telefono,correo)
                         )
                self.conexion.commit()
            return ["Perosnal asistencial creado exitosamente"], True 
        except Exception as e:
            return [f"error creandopersonal asistencial --> {e}"],False
    @wrapper_reconect
    def crear_usuario(self,nombre_completo,documento_identidad,correo,usuario,contraseña,contraseña_md5,cargo):
        print("crear usuario")
        try:
            nivel_acceso = self.niveles_acceso[cargo]
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
                                %s, 1,
                                %s, %s,
                                GETDATE(), '1', '', 0,0,
                                %s,
                                0,0, 0,0,0,0,0, 0,0,'','','')""",(
                                    usuario,documento_identidad,nombre_completo,
                                    nivel_acceso,
                                    correo,contraseña_md5,
                                    contraseña
                                ))
                self.conexion.commit()
            return ["Creacion usuario exitosa"],True
        except Exception as e:
            return [f"Creacion Usuario Fallida --> {e}"] ,False
#---------------------------------------------------------------------
