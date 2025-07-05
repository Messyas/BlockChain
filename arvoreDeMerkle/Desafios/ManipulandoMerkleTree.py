import hashlib
from typing import List, Optional

from arvoreDeMerkle.ExMerkleTree import hash_dado

def gen_hash(dado: str) -> str:
    return hashlib.sha256(dado.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, dados: List[str]):
        self.dados: List[str] = dados
        self.niveis: List[List[str]] = []
        self.__construir_arvore()

    def __construir_arvore(self):
        self.niveis.clear()
        if not self.dados or not any(d.strip() for d in self.dados):
            return
        
        nivel_atual = [gen_hash(d) for d in self.dados]
        self.niveis.append(nivel_atual)

        while len(nivel_atual) > 1:
            proximo_nivel = []
            for i in range(0, len(nivel_atual), 2):
                esquerda = nivel_atual[i]
                direita = nivel_atual[i + 1] if i + 1 < len(nivel_atual) else esquerda
                combinado = esquerda + direita
                proximo_nivel.append(gen_hash(combinado))
            nivel_atual = proximo_nivel
            self.niveis.append(nivel_atual)

    def raiz_merkle(self) -> Optional[str]:
        if self.niveis and self.niveis[-1]:
            return self.niveis[-1][0]
        return None

    def mostrar_arvore(self):
        if not self.niveis:
            print("Arvore sem nada")
            return
            
        for i, nivel in enumerate(self.niveis):
            print(f"Nível {i}:")
            for h in nivel:
                print(f"  {h}")
            print()

def simular_modificacao(dados: List[str]) -> bool:
    while True:
        resposta = input("Deseja simular uma modificação em um bloco? (s/n): ").lower()
        if resposta in ["s", "n"]:
            break
        print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
    
    if resposta == 'n':
        return False

    while True: #solitacao com base no index do bloco ->
        try:
            indice = int(input(f"Qual o índice do bloco a ser modificado? (0 a {len(dados)-1}): "))
            if 0 <= indice < len(dados):
                break
            else:
                print("Índice fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    novo_valor = input(f"Digite o novo valor para o bloco {indice} ('{dados[indice]}'): ")
    dados[indice] = novo_valor
    print("\nBloco de dados modificado com sucesso!")
    return True

if __name__ == "__main__":
    print("--- Criação da Árvore de Merkle ---")
    dados_entrada = input("Digite a lista de dados iniciais, separados por vírgula: ")
    dados = [d.strip() for d in dados_entrada.split(',') if d.strip()]

    if not dados:
        print("Nenhum dado fornecido. Encerrando o programa.")
    else:
        print("\nÁrvore de Merkle Original")
        arvore_original = MerkleTree(dados)
        raiz_original = arvore_original.raiz_merkle()
        
        print(f"Merkle Root: {raiz_original}\n")
        arvore_original.mostrar_arvore()

        if simular_modificacao(dados):
            print("\nÁrvore Recalculada Após Modificação")
            arvore_modificada = MerkleTree(dados)
            raiz_modificada = arvore_modificada.raiz_merkle()

            print(f"Novo Merkle Root: {raiz_modificada}\n")
            arvore_modificada.mostrar_arvore()

            print("--- Comparação ---")
            if raiz_original != raiz_modificada:
                print("Como esperado, o Merkle Root mudou, provando que os dados foram alterados.")
            else:
                print("O Merkle Root não mudou. Você alterou o bloco para o mesmo valor original?")

    print("\nPrograma finalizado.")