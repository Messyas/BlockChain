from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def gerrar_chave():
    """Gera um par de chaves RSA."""
    chave = RSA.generate(2048)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    return chave_privada, chave_publica