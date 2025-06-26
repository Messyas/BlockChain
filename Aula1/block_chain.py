import hashlib

def calcular_hash(bloco):
    bloco_str = f"{bloco['indice']}{bloco['dados']}{bloco['hash_anterior']}"
    return hashlib.sha256(bloco_str.encode()).hexdigest()

def criar_blockchain_valida():
    blockchain = []
    bloco_genese = {
        'indice': 0,
        'dados': 'Primeiro Bloco',
        'hash_anterior': '0',
    }
    bloco_genese['hash'] = calcular_hash(bloco_genese)
    blockchain.append(bloco_genese)
    for i in range(1, 6): # ate 6
        bloco_anterior = blockchain[-1]
        novo_bloco = {
            'indice': i,
            'dados': f'Dados do bloco {i}',
            'hash_anterior': bloco_anterior['hash'],
        }
        novo_bloco['hash'] = calcular_hash(novo_bloco)
        blockchain.append(novo_bloco)
    return blockchain

def validar_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        bloco_atual = blockchain[i]
        bloco_anterior = blockchain[i - 1]
        if bloco_atual['hash_anterior'] != bloco_anterior['hash']:
            print(f"FALHA: Inconsistência entre o bloco {bloco_anterior['indice']} e {bloco_atual['indice']}.")
            return False
        if bloco_atual['hash'] != calcular_hash(bloco_atual):
            return False
    return True

print("--- Teste 1 ---")
blockchain_cenario_1 = criar_blockchain_valida()
for bloco in blockchain_cenario_1:
    print(bloco)
print(f"\nBlockchain válida? {'Sim' if validar_blockchain(blockchain_cenario_1) else 'Não'}")
print("-" * 50)

blockchain_cenario_2 = criar_blockchain_valida()
print("Alterando dados do bloco 3...")
blockchain_cenario_2[3]['dados'] = "Dados Alterados"
print("Blockchain após tentativa de alteração:")
for bloco in blockchain_cenario_2:
    print(bloco)
print(f"\nBlockchain válida? {'Sim' if validar_blockchain(blockchain_cenario_2) else 'Não'}")
print("-" * 50)

blockchain_cenario_3 = criar_blockchain_valida()
blockchain_cenario_3[2]['dados'] = "Dados Alterados de forma 'inteligente'"
blockchain_cenario_3[2]['hash'] = calcular_hash(blockchain_cenario_3[2])
blockchain_cenario_3[3]['hash_anterior'] = blockchain_cenario_3[2]['hash']
for bloco in blockchain_cenario_3:
    print(bloco)
print(f"\nBlockchain válida? {'Sim' if validar_blockchain(blockchain_cenario_3) else 'Não'}")
print("-" * 50)

blockchain_cenario_4 = criar_blockchain_valida()
indice_bloco_alterado = 1
blockchain_cenario_4[indice_bloco_alterado]['dados'] = "Fraude"
for i in range(indice_bloco_alterado, len(blockchain_cenario_4)):
    if i > 0:
        blockchain_cenario_4[i]['hash_anterior'] = blockchain_cenario_4[i-1]['hash']
    blockchain_cenario_4[i]['hash'] = calcular_hash(blockchain_cenario_4[i])
for bloco in blockchain_cenario_4:
    print(bloco)
print(f"\nBlockchain válida? {'Sim' if validar_blockchain(blockchain_cenario_4) else 'Não'}")
print("-" * 50)