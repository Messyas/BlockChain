from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(texto):
    """Adiciona padding ao texto para que seu tamanho seja múltiplo de 16 bytes."""
    while len(texto) % 16 != 0:
        texto += ' '
    return texto

def cifrar_aes(texto, chave):
    """Cifra o texto usando AES com a chave fornecida."""
    cipher = AES.new(chave, AES.MODE_ECB)
    texto_padded = pad(texto)
    return cipher.encrypt(texto_padded.encode('utf-8'))

def decifrar_aes(texto_cifrado, chave):
    """Decifra o texto cifrado usando AES com a chave fornecida."""
    cipher = AES.new(chave, AES.MODE_ECB)
    texto_decifrado = cipher.decrypt(texto_cifrado).decode('utf-8')
    return texto_decifrado.rstrip()