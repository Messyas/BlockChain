const { ethers } = require("ethers");

const RPC_URL = "https://mainnet.infura.io/v3/";
const provider = new ethers.JsonRpcProvider(RPC_URL);

async function monitorarGasPrice() {
  try {
    const feeData = await provider.getFeeData();
    const gasPriceGwei = ethers.formatUnits(feeData.gasPrice, "gwei");
    const maxFeePerGasGwei = ethers.formatUnits(feeData.maxFeePerGas, "gwei");
    const maxPriorityFeePerGasGwei = ethers.formatUnits(
      feeData.maxPriorityFeePerGas,
      "gwei"
    );

    console.log(`------ ${new Date().toLocaleTimeString()} ------`);
    console.log(
      `Preço de Gás (Legado): ${parseFloat(gasPriceGwei).toFixed(2)} Gwei`
    );
    console.log(
      `Taxa Máxima por Gás (maxFeePerGas): ${parseFloat(
        maxFeePerGasGwei
      ).toFixed(2)} Gwei`
    );
    console.log(
      `Taxa de Prioridade (maxPriorityFeePerGas): ${parseFloat(
        maxPriorityFeePerGasGwei
      ).toFixed(2)} Gwei`
    );
    console.log("--------------------------------------");
  } catch (error) {
    console.error("Erro ao buscar o preço do gás:", error.message);
  }
}

console.log("Iniciando o monitor de Gas Price...");
monitorarGasPrice();
setInterval(monitorarGasPrice, 15000);
