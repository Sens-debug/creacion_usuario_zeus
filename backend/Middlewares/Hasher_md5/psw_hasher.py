import hashlib

def psw_hasher(psw):
# Convertir el string a bytes
    psw_bytes = psw.encode('utf-8')
    # Crear el hash MD5
    hash_md5 = hashlib.md5(psw_bytes)
    # Obtener el hash en formato hexadecimal
    hash_hex = hash_md5.hexdigest()
    return hash_hex