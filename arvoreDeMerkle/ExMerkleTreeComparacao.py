import hashlib
from typing import List, Optional

def hash_dado(dado: str) -> str:
    """Cria um hash SHA-256 para uma string de entrada."""
    return hashlib.sha256(dado.encode('utf-8')).hexdigest()

class MerkleTree:
    """
    Uma implementação de uma Árvore de Merkle para verificar a integridade de dados.
    """
    def __init__(self, dados: List[str]):
        """Inicializa e constrói a Árvore de Merkle com uma lista de dados."""
        self.dados: List[str] = dados
        self.niveis: List[List[str]] = []
        self.__construir_arvore()

    def __construir_arvore(self):
        """
        Constrói a árvore a partir dos dados. É chamado automaticamente na inicialização.
        """
        # Garante que a árvore esteja vazia antes de construir ou reconstruir
        self.niveis.clear()

        # Retorna se não houver dados válidos para processar
        if not self.dados or not any(self.dados):
            return

        nivel_atual = [hash_dado(d) for d in self.dados]
        self.niveis.append(nivel_atual)

        while len(nivel_atual) > 1:
            proximo_nivel = []
            for i in range(0, len(nivel_atual), 2):
                esquerda = nivel_atual[i]
                # Se houver um número ímpar de nós, o último nó é duplicado para formar um par
                direita = nivel_atual[i + 1] if i + 1 < len(nivel_atual) else esquerda
                combinado = esquerda + direita
                proximo_nivel.append(hash_dado(combinado))
            
            nivel_atual = proximo_nivel
            self.niveis.append(nivel_atual)

    def raiz_merkle(self) -> Optional[str]:
        """Retorna a raiz da Árvore de Merkle (o hash no topo da árvore)."""
        if self.niveis and self.niveis[-1]:
            return self.niveis[-1][0]
        return None

    def mostrar_arvore(self):
        """Exibe de forma legível todos os níveis e seus respectivos hashes."""
        if not self.niveis:
            print("A árvore está vazia (não há dados para exibir).")
            return
            
        for i, nivel in enumerate(self.niveis):
            print(f"Nível {i}:")
            for h in nivel:
                print(f"  {h}")
            print()

def obter_dados_para_arvore(numero_arvore: int) -> List[str]:
    """Solicita ao usuário que insira dados para uma árvore específica."""
    print(f"\n=== Dados para a Árvore {numero_arvore} ===")
    dados_entrada = input("Digite os dados separados por vírgula: ")
    # Retorna uma lista, tratando o caso de entrada vazia
    return [d.strip() for d in dados_entrada.split(",") if d.strip()]

# --- Programa Principal ---
if __name__ == "__main__":
    # Coleta de dados para as duas árvores
    lista_dados_1 = obter_dados_para_arvore(1)
    lista_dados_2 = obter_dados_para_arvore(2)

    # Criação das árvores de Merkle
    arvore1 = MerkleTree(lista_dados_1)
    arvore2 = MerkleTree(lista_dados_2)

    # Exibição da primeira árvore
    print("\n--- Primeira Árvore de Merkle ---")
    arvore1.mostrar_arvore()
    raiz1 = arvore1.raiz_merkle()
    print(f"Merkle Root 1: {raiz1}\n")

    # Exibição da segunda árvore
    print("\n--- Segunda Árvore de Merkle ---")
    arvore2.mostrar_arvore()
    raiz2 = arvore2.raiz_merkle()
    print(f"Merkle Root 2: {raiz2}\n")

    # Comparação final das raízes
    print("--- Resultado da Comparação ---")
    if raiz1 and raiz1 == raiz2:
        print("As Raízes de Merkle são IDÊNTICAS.")
        print("Isso indica que os conjuntos de dados originais são os mesmos.")
    else:
        print("As Raízes de Merkle são DIFERENTES.")
        print("Isso indica que os conjuntos de dados foram alterados ou são distintos.")