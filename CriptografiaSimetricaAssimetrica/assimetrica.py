from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
 
def gen_chave():
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
def decifrar(texto_cifrado, chave_privada):
    """Decifra um texto cifrado usando a chave privada RSA."""
    rsa_chave_privada = RSA.import_key(chave_privada)
    cipher = PKCS1_OAEP.new(rsa_chave_privada)
    texto_decifrado = cipher.decrypt(texto_cifrado)
    return texto_decifrado.decode()

if __name__ == "__main__":
    chave_privada, chave_publica = gen_chave()
    texto = "suas melhores palavras hohoho"
    texto_cifrado = cifrar(texto, chave_publica)
    texto_decifrado = decifrar(texto_cifrado, chave_privada)
    print("Texto original:", texto)
    print("Texto cifrado:", texto_cifrado)
    print("Texto decifrado:", texto_decifrado)