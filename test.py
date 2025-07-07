import hashlib

texto = "123456789"
# Convertir el string a bytes
texto_bytes = texto.encode('utf-8')

# Crear el hash MD5
hash_md5 = hashlib.md5(texto_bytes)

# Obtener el hash en formato hexadecimal
hash_hex = hash_md5.hexdigest()

if hash_hex=='25f9e794323b453885f5181f1b624d0b':
    print("igual")
print(hash_hex)