import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_credenciales_gmail(correo_destinatario,usuario_zeus,contraseña_zeus,cargo,nombre_completo):
    '''Retorna [Mensaje] y Boolean'''
    try:
        json_mensjaes = {
"ANTIBIOTICOTERAPIA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\antibiotic_template.html",
"AUXILIAR ENFERMERIA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\nurse_template.html",
"CUIDADOR":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\nurse_template.html",
"MEDICINA GENERAL":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\doctor_template.html",
"MEDICINA GENERAL MEDIO TIEMPO":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\doctor_template.html",
"TERAPIA FISICA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"TERAPIA OCUPACIONAL":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"TERAPIA FONOAUDIOLOGICA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"TERAPIA GENERAL":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"TERAPIA RESPIRATORIA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"PSICOLOGIA":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
"NUTRICION":"C:\\Users\\Sistemas\\Desktop\\Repositorios IPSTID\\creacion_usuario_zeus\\backend\\Middlewares\\Mail_Sender\\msg_templates\\pro_employe_template.html",
}
        remitente = "cuentaszeusipstid@gmail.com"
        destinatario= correo_destinatario
        contraseña = "wjvm wzsk tcft kzpq"
        asunto= "CREDENCIALES ACCESO ZEUS"

        with open (json_mensjaes[cargo],'r',encoding='utf-8') as file:
            cuerpo_html=file.read().format(cargo=cargo,usuario_zeus=usuario_zeus,contraseña_zeus=contraseña_zeus,nombre_completo=nombre_completo)

        cuerpo = json_mensjaes[cargo]
        mensaje = MIMEMultipart('alternative')
        mensaje["From"]=remitente
        mensaje["To"]=destinatario
        mensaje["subject"]=asunto
        parte_html= MIMEText(cuerpo_html,'html')
        mensaje.attach(parte_html)

        with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
            smtp.login(remitente,contraseña)
            smtp.sendmail(remitente,destinatario,mensaje.as_string())
            print("enviado")
        return ["Correo enviado exitosamente"],True
    except Exception as e:
        print("error")
        print(e)
        return [f"Error enviando el correo---> {e}"], False
    
