def generate_username(l_nombres):
    '''Recibe lista de nombres ordenada\n
[p_n, s_n, p_a, s_a]\n
Retorna String con el username, y boolean'''
    nombre_completisimo = True if len(l_nombres)>=4 else False
    if nombre_completisimo:
        r =f"{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2].upper()}{l_nombres[3][0].upper()}"
        return r.replace(" ","")
    else:
        r =f"{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2].upper()}{l_nombres[3][0].upper()}"
        return r.replace(" ","")
        


def generate_psw(l_nombres,numero_documento):
    '''Recibe lista de nombres ordenada y un numero de documento\n
[p_n, s_n, p_a, s_a]\n
Retorna String con la password y boolean'''
    # ultimos_4_digitos_cedula = numero_documento[-4:]
    nombre_completisimo = True if len(l_nombres)>=4 else False 
    if nombre_completisimo:
        p=f"{numero_documento[-4:]}{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2][0].upper()}{l_nombres[3][0].upper()}"
        return p.replace(" ","")
    else:
        p= f"{numero_documento[-4:]}{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2][0].upper()}"
        return p.replace(" ","")

def generate_creds(lista_nombres,numero_documento):
    '''Recibe una lista de nombres y un numeor de documento\n
Retorna [Username,Password] o [ERROR]'''
    try:
        return [generate_username(lista_nombres),generate_psw(lista_nombres,numero_documento)]
    except Exception as e:
        return [f"Error en generate creds --> {e}"]

