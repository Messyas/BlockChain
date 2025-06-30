from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def gerrar_chave():
    """Gera um par de chaves RSA."""
    chave = RSA.generate(2048)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    return chave_privada, chave_publica

def cifrar(texto, chave_publica):
    """Cifra um texto usando a chave pública RSA."""
    rsa_chave_publica = RSA.import_key(chave_publica)
    cipher = PKCS1_OAEP.new(rsa_chave_publica)
    texto_cifrado = cipher.encrypt(texto.encode())
    return texto_cifrado
