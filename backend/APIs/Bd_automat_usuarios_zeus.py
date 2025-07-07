import mysql.connector
from backend.Middlewares.SaaS.SaaS import saas

class ConexionAutomatUsuarioZeus(mysql.connector.MySQLConnection):
    def __init__(self):
        config={
            'host':'localhost',
            'user':'root',
            'password':'',
            'database':'automat_usuarios_zeus'
        }
        super().__init__(**config)
    
    def revisar_conexion(funcion_envuelta):
        '''Funcion Decoradora\n
        Si la conexion está cerrada, la re-abre con la misma configuracion de la instacian\n
        Comprueba el SaaS'''
        def envoltura(self,*args,**kwargs):
            control = saas()
            if not self.is_connected():
                self.connect()
            resultado = funcion_envuelta(self,*args,**kwargs)
            self.disconnect()
            return resultado, control
        return envoltura
    
    @revisar_conexion
    def comprobar_estado_funcionamiento(self):
        '''Retorna Boolean'''
        with self.cursor() as cursor:
            cursor.execute("select * from control_funcion")
            ret = cursor.fetchall()
            if not ret or ret[0][0]==0:
                return False
            elif ret[0][0]==1:
                return True
    
    def registrar_empleado_creado(self,primer_nombre,segundo_nombre,primer_apellido_segundo_apellido,
                                  nombre_completo,correo,telefono,documento_identidad,especialidad):
        pass
