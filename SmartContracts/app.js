import { ethers } from "ethers";

const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();

const abiGerenciamentoDeUsuarios = [
  "event UsuarioAdicionado(address indexed endereco, string nome, uint idade, string email)",
  "event UsuarioAtualizado(address indexed endereco, string nome, uint idade, string email)",
  "function adicionarUsuario(string memory _nome, uint _idade, string memory _email) public",
  "function atualizarUsuario(string memory _nome, uint _idade, string memory _email) public",
  "function buscarUsuario(address _endereco) public view returns (string memory, uint, string memory)",
  "function usuarios(address) public view returns (string, uint, string, bool)",
];

const enderecoContrato = "0x...";
const contrato = new ethers.Contract(
  enderecoContrato,
  abiGerenciamentoDeUsuarios,
  signer
);

async function adicionarNovoUsuario(nome, idade, email) {
  try {
    console.log("Enviando transação para adicionar usuário...");
    const tx = await contrato.adicionarUsuario(nome, idade, email);
    await tx.wait();
    console.log("Usuário adicionado com sucesso! Hash da transação:", tx.hash);
  } catch (error) {
    console.error("Erro ao adicionar usuário:", error);
  }
}
async function buscarUmUsuario(endereco) {
  try {
    console.log(`Buscando dados do usuário no endereço ${endereco}`);
    const [nome, idade, email] = await contrato.buscarUsuario(endereco);

    console.log("--- Dados do Usuário ---");
    console.log(`Nome: ${nome}`);
    console.log(`Idade: ${Number(idade)}`);
    console.log(`Email: ${email}`);
    console.log("-----------------------");
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
  }
}

function escutarEventos() {
  console.log("Escutando eventos do contrato...");
  contrato.on("UsuarioAdicionado", (endereco, nome, idade, email, event) => {
    console.log("🎉 Evento 'UsuarioAdicionado' detectado!");
    console.log(`  Endereço: ${endereco}`);
    console.log(`  Nome: ${nome}`);
    console.log(`  Idade: ${Number(idade)}`);
    console.log(`  Email: ${email}`);
  });
}

(async () => {
  escutarEventos();
  await adicionarNovoUsuario("Alice", 30, "alice@email.com");
  const meuEndereco = await signer.getAddress();
  await buscarUmUsuario(meuEndereco);
})();
