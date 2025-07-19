async function estimarGasDaTransacao(txObjeto) {
  try {
    console.log("\nEstimando gás para a transação...");
    const gasEstimado = await provider.estimateGas(txObjeto);
    console.log(`Gás estimado (Gas Limit): ${gasEstimado.toString()}`);
    return gasEstimado;
  } catch (error) {
    console.error("Erro ao estimar o gás:", error.message);
    throw error;
  }
}

async function exemploDeEstimativa() {
    const transacaoExemplo = {
        to: "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B", 
        value: ethers.parseEther("0.01")
    };

    try {
        const gasLimit = await estimarGasDaTransacao(transacaoExemplo);
        const feeData = await provider.getFeeData();
        const custoTotalEstimadoWei = gasLimit * feeData.gasPrice;
        const custoTotalEstimadoEth = ethers.formatEther(custoTotalEstimadoWei);

        console.log(`\nCusto total estimado da transação:`);
        console.log(`${custoTotalEstimadoEth} ETH`);
        console.log(`(Com base no preço de gás legado de ${ethers.formatUnits(feeData.gasPrice, "gwei")} Gwei)`);
    } catch (error) {
       console.log(error)
    }
}

exemploDeEstimativa();