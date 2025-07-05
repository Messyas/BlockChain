import hashlib

def hash_dado(dado: str) -> str:
    """Cria um hash SHA-256 para um dado de entrada."""
    return hashlib.sha256(dado.encode('utf-8')).hexdigest()

class MerkleTree:
    """
    Uma implementação de uma Árvore de Merkle que se reconstrói
    quando os dados são modificados.
    """
    def __init__(self, dados: list):
        """Inicializa a Árvore de Merkle com uma lista de dados."""
        self.dados = dados
        self.niveis = []
        self.__construir_arvore()

    def __construir_arvore(self):
        """Constrói a Árvore de Merkle a partir dos dados atuais."""
        if not self.dados or not any(self.dados):
            self.niveis = []
            return

        # Limpa os níveis anteriores para reconstrução
        self.niveis.clear()

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

    def raiz_merkle(self) -> str | None:
        """Retorna a raiz da Árvore de Merkle (o hash final)."""
        return self.niveis[-1][0] if self.niveis and self.niveis[-1] else None

    def mostrar_arvore(self):
        """Exibe todos os níveis e seus respectivos hashes na árvore."""
        for i, nivel in enumerate(self.niveis):
            print(f"Nível {i}:")
            # Adiciona uma verificação para não imprimir hashes vazios se o nível estiver vazio
            if nivel:
                for h in nivel:
                    print(f"  {h}")
            print()

def obter_dados_do_usuario() -> list:
    """Pede ao usuário para inserir dados e retorna uma lista."""
    dados_entrada = input("Digite os dados separados por vírgula: ")
    return [d.strip() for d in dados_entrada.split(",")]

def modificar_dados(dados: list) -> bool:
    """Permite ao usuário modificar um item na lista de dados."""
    while True:
        alterar = input("Deseja modificar algum bloco de dados? (s/n): ").lower()
        if alterar in ["s", "n"]:
            break
        print("Resposta inválida. Por favor, digite 's' ou 'n'.")

    if alterar == "s":
        while True:
            try:
                indice = int(input(f"Qual o índice do bloco para modificar? (0 a {len(dados)-1}): "))
                if 0 <= indice < len(dados):
                    novo_valor = input("Digite o novo valor para o bloco: ")
                    dados[indice] = novo_valor
                    return True
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro para o índice.")
    return False

# --- Programa Principal ---
if __name__ == "__main__":
    dados_iniciais = obter_dados_do_usuario()
    
    # Cria e exibe a árvore inicial
    arvore = MerkleTree(dados_iniciais)
    print("\n=== Árvore de Merkle Original ===")
    arvore.mostrar_arvore()
    print(f"Merkle Root Original: {arvore.raiz_merkle()}\n")

    # Verifica se o usuário quer modificar os dados e reconstrói a árvore se necessário
    if modificar_dados(dados_iniciais):
        # A lista `dados_iniciais` foi modificada pela função `modificar_dados`.
        # Agora, criamos uma nova árvore com os dados atualizados.
        arvore_modificada = MerkleTree(dados_iniciais)
        print("\n=== Nova Árvore de Merkle (Após Modificação) ===")
        arvore_modificada.mostrar_arvore()
        print(f"Novo Merkle Root: {arvore_modificada.raiz_merkle()}\n")

    print("Programa finalizado.")