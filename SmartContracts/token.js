const abiToken = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function balanceOf(address) view returns (uint)",
  "function mint(address to, uint256 amount)",
  "function burn(uint256 amount)",
  "event Transfer(address indexed from, address indexed to, uint256 value)",
];

const enderecoToken = "0x...";
const contratoToken = new ethers.Contract(enderecoToken, abiToken, signer);

async function criarNovosTokens(destinatario, quantidade) {
  try {
    const quantidadeWei = ethers.parseUnits(quantidade.toString(), 18);
    const tx = await contratoToken.mint(destinatario, quantidadeWei);
    await tx.wait();
    console.log(`${quantidade} tokens criados para ${destinatario}`);
  } catch (error) {
    console.error("Erro ao criar tokens:", error);
  }
}

async function queimarTokens(quantidade) {
  try {
    const quantidadeWei = ethers.parseUnits(quantidade.toString(), 18);
    const tx = await contratoToken.burn(quantidadeWei);
    await tx.wait();
    console.log(`${quantidade} tokens foram queimados da sua conta.`);
  } catch (error) {
    console.error("Erro ao queimar tokens:", error);
  }
}

async function checarSaldo(endereco) {
  const saldoWei = await contratoToken.balanceOf(endereco);
  console.log(
    `Saldo de ${endereco}: ${ethers.formatUnits(saldoWei, 18)} tokens`
  );
}
