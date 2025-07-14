def generate_username(l_nombres):
    '''Recibe lista de nombres ordenada\n
[p_n, s_n, p_a, s_a]\n
Retorna String con el username, y boolean'''
    nombre_completisimo = True if len(l_nombres)>=4 else False
    if nombre_completisimo:
        return f"{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2].upper()}{l_nombres[3][0].upper()}"
    else:
        return f"{l_nombres[0][0].upper()}{l_nombres[1].upper()}{l_nombres[2][0].upper()}"


def generate_psw(l_nombres,numero_documento):
    '''Recibe lista de nombres ordenada y un numero de documento\n
[p_n, s_n, p_a, s_a]\n
Retorna String con la password y boolean'''
    # ultimos_4_digitos_cedula = numero_documento[-4:]
    nombre_completisimo = True if len(l_nombres)>=4 else False 
    if nombre_completisimo:
        return f"{numero_documento[-4:]}{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2][0].upper()}{l_nombres[3][0].upper()}"
    else:
        return f"{numero_documento[-4:]}{l_nombres[0][0].upper()}{l_nombres[1][0].upper()}{l_nombres[2][0].upper()}"

def generate_creds(lista_nombres,numero_documento):
    '''Recibe una lista de nombres y un numeor de documento\n
Retorna [Username,Password] o [ERROR]'''
    try:
        return [generate_username(lista_nombres),generate_psw(lista_nombres,numero_documento)]
    except Exception as e:
        return [e]

