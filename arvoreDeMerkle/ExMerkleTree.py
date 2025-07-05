import hashlib

def hash_dado(dado):
    """Cria um hash SHA-256 para um dado de entrada."""
    return hashlib.sha256(dado.encode('utf-8')).hexdigest()

class MerkleTree:
    """
    Uma implementação simples de uma Árvore de Merkle.
    """
    def __init__(self, dados):
        """
        Inicializa a Árvore de Merkle com uma lista de dados.
        """
        self.dados = dados
        self.niveis = []
        self.__construir_arvore()

    def __construir_arvore(self):
        """
        Constrói a Árvore de Merkle a partir dos dados iniciais.
        """
        if not self.dados:
            return

        nivel_atual = [hash_dado(d) for d in self.dados]
        self.niveis.append(nivel_atual)

        while len(nivel_atual) > 1:
            proximo_nivel = []
            for i in range(0, len(nivel_atual), 2):
                esquerda = nivel_atual[i]
                # Se houver um número ímpar de nós, duplica o último para o par.
                direita = nivel_atual[i + 1] if i + 1 < len(nivel_atual) else esquerda
                combinado = esquerda + direita
                proximo_nivel.append(hash_dado(combinado))
            
            self.niveis.append(proximo_nivel)
            nivel_atual = proximo_nivel

    def raiz_merkle(self):
        """
        Retorna a raiz da Árvore de Merkle (o hash final).
        """
        return self.niveis[-1][0] if self.niveis and self.niveis[-1] else None

    def mostrar_arvore(self):
        """
        Exibe todos os níveis e seus respectivos hashes na árvore.
        """
        print("Estrutura da Árvore de Merkle:")
        for i, nivel in enumerate(self.niveis):
            print(f"Nível {i}:")
            for h in nivel:
                print(f"  {h}")
            print()

# Exemplo de uso
if __name__ == "__main__":
    dados = ["Bloco1", "Bloco2", "Bloco3", "Bloco4", "Bloco5"]
    
    arvore = MerkleTree(dados)
    
    print(f"Raiz de Merkle: {arvore.raiz_merkle()}\n")
    arvore.mostrar_arvore()