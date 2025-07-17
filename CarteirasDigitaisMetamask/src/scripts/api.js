const NETWORKS = {
  "0x1": { name: "Ethereum Mainnet", currencySymbol: "ETH" },
  "0xaa36a7": { name: "Sepolia Testnet", currencySymbol: "SepoliaETH" },
  "0x5": { name: "Goerli Testnet", currencySymbol: "GoerliETH" },
  "0x89": { name: "Polygon Mainnet", currencySymbol: "MATIC" },
};

export function isMetaMaskInstalled() {
  return typeof window.ethereum !== "undefined";
}

export async function connectWallet() {
  if (!isMetaMaskInstalled()) {
    throw new Error(
      "MetaMask não está instalado. Por favor, instale a extensão."
    );
  }
  try {
    const accounts = await window.ethereum.request({
      method: "eth_requestAccounts",
    });
    if (accounts.length === 0) {
      throw new Error(
        "Nenhuma conta encontrada. Por favor, crie ou importe uma conta no MetaMask."
      );
    }
    return accounts;
  } catch (error) {
    console.error("Connection failed:", error);
    throw new Error("O usuário rejeitou a conexão da carteira.");
  }
}

export async function getBalance(accountAddress) {
  if (!accountAddress) throw new Error("Endereço da conta é necessário.");
  try {
    const balanceWei = await window.ethereum.request({
      method: "eth_getBalance",
      params: [accountAddress, "latest"],
    });

    const balanceEth = parseFloat(balanceWei) / 10 ** 18;
    return balanceEth.toFixed(4);
  } catch (error) {
    console.error("Failed to get balance:", error);
    throw new Error("Não foi possível obter o saldo da conta.");
  }
}

export async function getNetwork() {
  try {
    const chainId = await window.ethereum.request({ method: "eth_chainId" });
    const networkInfo = NETWORKS[chainId] || {
      name: `Rede Desconhecida (ID: ${chainId})`,
      currencySymbol: "ETH",
    };
    return { id: chainId, ...networkInfo };
  } catch (error) {
    console.error("Failed to get network:", error);
    throw new Error("Não foi possível obter a rede atual.");
  }
}

export async function switchNetwork(chainId) {
  if (!chainId) throw new Error("Chain ID é necessário.");
  try {
    await window.ethereum.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: chainId }],
    });
  } catch (switchError) {
    console.error("Failed to switch network:", switchError);
    throw new Error(`Falha ao trocar de rede. Erro: ${switchError.message}`);
  }
}
