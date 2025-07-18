import smtplib
from email.message import EmailMessage



def enviar_credenciales_gmail(correo_destinatario,usuario_zeus,contraseña_zeus,cargo,nombre_completo):
    '''Retorna [Mensaje] y Boolean'''
    try:
        json_mensjaes = {
"ANTIBIOTICOTERAPIA":F""" !!!  IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA  !!!
                         

🤖 Hola {nombre_completo}, te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

ESPERAMOS QUE TENGAS UNA GRAN AVENTURA EN TU CARGO COMO --> {cargo}

Proceso Confirmacion Citas

https://drive.google.com/file/d/1OeulemhO4pzJ5Kxk3yZ5_hsnLSaYA0t1/view?usp=drive_link

Cargue Notas Antibioticos 

https://drive.google.com/file/d/1OtQ4AMvg5yZB-svmrATrKcHf1MVxMLDx/view?usp=drive_link""",


"AUXILIAR ENFERMERIA":F""" !!!  IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA  !!!

🤖 Hola, {nombre_completo} te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

ESPERAMOS QUE TENGAS UNA GRAN AVENTURA EN TU CARGO COMO --> {cargo}

Guia Cargue Notas ZeusSalud

https://drive.google.com/file/d/1Ot-jfrO6u8U0gJUDNjSRWFMlnxoEvkt5/view?usp=drive_link"""
,

"MEDICINA GENERAL":f"""
 !!!  IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA  !!!

🤖 Hola, {nombre_completo} te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

ESPERAMOS QUE TENGAS UNA GRAN AVENTURA EN TU CARGO COMO --> {cargo}

Proceso confirmacion cita 
https://drive.google.com/file/d/1OeulemhO4pzJ5Kxk3yZ5_hsnLSaYA0t1/view?usp=drive_link

-----------------------------
Guia Historia Clinica Medicos

https://drive.google.com/file/d/1Os08deIEg_JEkn-CmJmddYfe1Rh-qDRm/view?usp=drive_link"""
,

"MEDICINA GENERAL MEDIO TIEMPO":F"""!!!  IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA  !!!

🤖 Hola, {nombre_completo} te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

ESPERAMOS QUE TENGAS UNA GRAN AVENTURA EN TU CARGO COMO --> {cargo}

Proceso confirmacion cita 
https://drive.google.com/file/d/1OeulemhO4pzJ5Kxk3yZ5_hsnLSaYA0t1/view?usp=drive_link
-----------------------------
Guia Historia Clinica Medicos

https://drive.google.com/file/d/1Os08deIEg_JEkn-CmJmddYfe1Rh-qDRm/view?usp=drive_link""",

"TERAPIA FISICA":f"""
!!!  IPSTID, SOMOS TÚ, SOMOS TODOS.
BIENVENID@ A NUESTRA GRAN FAMILIA  !!!

🤖 Hola, {nombre_completo} te entrego tu:

Usuario Plataforma Zeus Salud --> {usuario_zeus}
Contraseña Plataforma Zeus Salud --> {contraseña_zeus}
Acceso a la plataforma Zeus Salud --> http://bit.ly/eZeusSalud

ESPERAMOS QUE TENGAS UNA GRAN AVENTURA EN TU CARGO COMO --> {cargo}

Proceso confirmacion Citas 

https://drive.google.com/file/d/1OeulemhO4pzJ5Kxk3yZ5_hsnLSaYA0t1/view?usp=drive_link

---------------------------------------

Guia Notas [Nutricion-Terapia-Psicologia]

https://drive.google.com/file/d/1OxluWzrRBGWMH0edA5s6YJE9GWfXSEwf/view?usp=drive_link"""

}
        remitente = "cuentaszeusipstid@gmail.com"
        destinatario= correo_destinatario
        contraseña = "wjvm wzsk tcft kzpq"
        asunto= "CREDENCIALES ACCESO ZEUS"
        cuerpo = json_mensjaes[cargo]
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
    


