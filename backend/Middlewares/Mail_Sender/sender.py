import smtplib
from email.message import EmailMessage

def enviar_credenciales_gmail_antibiotico(correo_destinatario,usuario_zeus,contraseña_zeus):
    '''Retorna [Mensaje] y Boolean'''
    try:
        remitente = "cuentaszeusipstid@gmail.com"
        destinatario= correo_destinatario
        contraseña = "wjvm wzsk tcft kzpq"
        asunto= "CREDENCIALES ACCESO ZEUS"
        cuerpo = f""" !!!IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA !!!

🤖 Hola, te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

Proceso Confirmacion Citas

https://drive.google.com/file/d/1OeulemhO4pzJ5Kxk3yZ5_hsnLSaYA0t1/view?usp=drive_link

Cargue Notas Antibioticos 

https://drive.google.com/file/d/1OtQ4AMvg5yZB-svmrATrKcHf1MVxMLDx/view?usp=drive_link"""
        mensaje = EmailMessage()
        mensaje["From"]=remitente
        mensaje["To"]=destinatario
        mensaje["subject"]=asunto
        mensaje.set_content(cuerpo)

        with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
            smtp.login(remitente,contraseña)
            smtp.send_message(mensaje)
        return ["Correo enviado exitosamente"],True
    except Exception as e:
        return [f"Error enviando el correo---> {e}"], False
    
