from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def cifrar(texto, chave):
    """Cifra usando AES com padding PKCS#7."""
    cipher = AES.new(chave, AES.MODE_ECB)
    texto_bytes = texto.encode('utf-8')
    texto_padded = pad(texto_bytes, AES.block_size)
    return cipher.encrypt(texto_padded)

def decifrar(texto_cifrado, chave):
    """Decifra usando AES"""
    cipher = AES.new(chave, AES.MODE_ECB)
    texto_padded_decifrado = cipher.decrypt(texto_cifrado)
    texto_original_bytes = unpad(texto_padded_decifrado, AES.block_size)
    return texto_original_bytes.decode('utf-8')

if __name__ == "__main__":
    chave = get_random_bytes(16)  
    texto = "é medo ou coragem, que te motiva ser de carne?"
    print(f"Texto original: {texto}")
    
    # Cifragem
    texto_cifrado = cifrar(texto, chave)
    print(f"Texto cifrado: {texto_cifrado.hex()}")
    
    # Decifragem
    texto_decifrado = decifrar(texto_cifrado, chave)
    print(f"Texto decifrado: {texto_decifrado}")
