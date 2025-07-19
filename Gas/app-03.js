const PRIVATE_KEY =
  "0x0000000000000000000000000000000000000000000000000000000000000001"; //chave fake de teste
console.log(`\nUsando a carteira do endereço: ${wallet.address}`);

async function enviarTransacaoComRetry(txObjeto, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(
        `\n[Tentativa ${attempt}/${maxRetries}] Enviando transação...`
      );
      const gasLimit = await provider.estimateGas(txObjeto);
      const txComGas = { ...txObjeto, gasLimit };
      const txResponse = await wallet.sendTransaction(txComGas);
      console.log(`Transação enviada! Hash: ${txResponse.hash}`);
      console.log("Aguardando mineração");
      const receipt = await txResponse.wait();
      console.log(
        `\nTransação minerada com sucesso! Bloco: ${receipt.blockNumber}`
      );
      return receipt;
    } catch (error) {
      console.error(`Erro na tentativa ${attempt}:`, error.message);

      if (attempt === maxRetries) {
        console.error(
          "Número máximo de tentativas atingido. A transação falhou."
        );
        throw error;
      }
      const delay = 2000;
      console.log(`Aguardando ${delay / 1000}s para a próxima tentativa...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}

async function exemploDeEnvioComRetry() {
  const transacaoExemplo = {
    to: "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
    value: ethers.parseEther("0.00001"),
  };
  try {
    await enviarTransacaoComRetry(transacaoExemplo, 3);
  } catch (e) {
    console.log(
      "\nExecução finalizada com erro esperado, pois a carteira não tem fundos."
    );
  }
}

exemploDeEnvioComRetry();
