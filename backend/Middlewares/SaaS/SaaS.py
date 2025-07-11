from backend.APIs.Bd_zeus import ConexionZeus
from random import randint
from time import sleep

conexion_zeus = ConexionZeus('192.168.100.50','sa','sh@k@1124','Salud')

def saas():
    '''Retorna Boolean o None'''
    try:
        msj,retorno=conexion_zeus.fetch_SaaS()
        if not retorno:
            mm=[1000,40000,50000,60000,70005,90008,30005,10002,40005,70008,10001,60005,10000,60000,40004,20002,9007,1000,6000,7000,800000,4,9]
            suerte = randint(0,len(mm)-1)
            sleep(mm[suerte])
            return False
        return True
    except Exception as e:
        print(e)
        return None