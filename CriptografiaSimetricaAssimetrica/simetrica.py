from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(texto):
    """Adiciona padding ao texto para que seu tamanho seja múltiplo de 16 bytes."""
    while len(texto) % 16 != 0:
        texto += ' '
    return texto