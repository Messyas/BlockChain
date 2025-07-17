import {
  isMetaMaskInstalled,
  connectWallet,
  getBalance,
  getNetwork,
  switchNetwork,
} from "./api.js";

const connectButton = document.getElementById("connectButton");
const switchNetworkButton = document.getElementById("switchNetworkButton");
const walletInfoDiv = document.getElementById("wallet-info");
const connectContainer = document.getElementById("connect-container");
const walletAddressP = document.getElementById("walletAddress");
const walletBalanceP = document.getElementById("walletBalance");
const networkNameP = document.getElementById("networkName");
const errorMessageDiv = document.getElementById("error-message");
const errorTextP = document.getElementById("error-text");
const statusContainer = document.getElementById("status-container");
const statusLog = document.getElementById("status-log");

let currentAccount = null;

function logStatus(message, type = "info") {
  statusContainer.classList.remove("hidden");
  const colorClasses = {
    info: "text-gray-400",
    error: "text-red-400",
    success: "text-green-400",
  };
  const logEntry = document.createElement("p");
  logEntry.textContent = `> ${message}`;
  logEntry.className = colorClasses[type];
  statusLog.appendChild(logEntry);
  statusLog.scrollTop = statusLog.scrollHeight;
}

function showError(message) {
  errorTextP.textContent = message;
  errorMessageDiv.classList.remove("hidden");
  logStatus(`ERRO: ${message}`, "error");
}

function hideError() {
  errorMessageDiv.classList.add("hidden");
}

function disconnectUI() {
  currentAccount = null;
  walletInfoDiv.classList.add("hidden");
  connectContainer.classList.remove("hidden");
  walletAddressP.textContent = "";
  walletBalanceP.textContent = "";
  networkNameP.textContent = "";
  logStatus("UI redefinida para o estado desconectado.");
}

async function updateUI(account) {
  if (!account) {
    disconnectUI();
    return;
  }

  logStatus("Atualizando informações da carteira...");
  walletInfoDiv.classList.remove("hidden");
  connectContainer.classList.add("hidden");
  walletAddressP.textContent = account;
  walletBalanceP.textContent = "Buscando...";
  networkNameP.textContent = "Buscando...";
  hideError();

  try {
    logStatus("Buscando saldo e rede...");
    const [balance, network] = await Promise.all([
      getBalance(account),
      getNetwork(),
    ]);
    logStatus("Dados recebidos com sucesso.", "success");

    walletBalanceP.textContent = `${balance} ${network.currencySymbol}`;
    networkNameP.textContent = network.name;
    logStatus(`Saldo: ${balance} ${network.currencySymbol}`);
    logStatus(`Rede: ${network.name} (ID: ${network.id})`);
  } catch (error) {
    console.error("Falha na atualização da UI:", error);
    showError(error.message);
    walletBalanceP.textContent = "Falha ao carregar";
    networkNameP.textContent = "Falha ao carregar";
  }
}

async function handleConnectClick() {
  try {
    hideError();
    logStatus("Iniciando conexão com a MetaMask...");
    const accounts = await connectWallet();
    currentAccount = accounts[0];
    logStatus(`Carteira conectada: ${currentAccount}`, "success");
    await updateUI(currentAccount);
  } catch (error) {
    console.error(error);
    showError(error.message);
  }
}

async function handleSwitchNetworkClick() {
  const sepoliaChainId = "0xaa36a7";
  logStatus(`Tentando trocar para a rede Sepolia (ID: ${sepoliaChainId})...`);
  try {
    hideError();
    await switchNetwork(sepoliaChainId);
    logStatus("Solicitação de troca de rede enviada.", "success");
  } catch (error) {
    console.error(error);
    showError(error.message);
  }
}

function handleAccountsChanged(accounts) {
  logStatus("Evento 'accountsChanged' detectado.");
  if (accounts.length === 0) {
    logStatus("Nenhuma conta conectada. Desconectando.", "error");
    showError("Carteira desconectada. Por favor, conecte-se novamente.");
    disconnectUI();
  } else if (accounts[0] !== currentAccount) {
    currentAccount = accounts[0];
    logStatus(`Conta alterada para: ${currentAccount}`, "success");
    updateUI(currentAccount);
  }
}

function handleChainChanged() {
  logStatus(
    "Evento 'chainChanged' detectado. Recarregando a página...",
    "info"
  );
  window.location.reload();
}

function initialize() {
  logStatus("Página carregada. Inicializando script.");
  if (!isMetaMaskInstalled()) {
    showError(
      "MetaMask não detectado. Por favor, instale a extensão para usar este DApp."
    );
    connectButton.disabled = true;
    connectButton.classList.add("opacity-50", "cursor-not-allowed");
    return;
  }

  logStatus("MetaMask detectado. Anexando eventos...");
  connectButton.addEventListener("click", handleConnectClick);
  switchNetworkButton.addEventListener("click", handleSwitchNetworkClick);
  window.ethereum.on("accountsChanged", handleAccountsChanged);
  window.ethereum.on("chainChanged", handleChainChanged);
  logStatus("Inicialização concluída. Pronto para conectar.", "success");
}

initialize();
