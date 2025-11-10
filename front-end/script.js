const micBtn = document.getElementById("micBtn");
const texto = document.getElementById("texto");
const cameraBtn = document.getElementById("cameraBtn");
const helpBtn = document.getElementById("helpBtn");
const assistente = document.getElementById("voiceAssist");
let gravando = false;

// Função para falar texto
function falar(mensagem) {
  const fala = new SpeechSynthesisUtterance(mensagem);
  fala.lang = "pt-BR";
  speechSynthesis.speak(fala);
}

// Foco de teclado lê o nome do botão
document.querySelectorAll("button").forEach((btn) => {
  btn.addEventListener("focus", () => {
    const label = btn.getAttribute("aria-label");
    if (label) falar(label);
  });
});

// Microfone (ativa/desativa gravação)
micBtn.addEventListener("click", () => {
  gravando = !gravando;
  micBtn.classList.toggle("active");

  if (gravando) {
    falar("Gravando. Pode falar agora.");
    texto.textContent = "Gravando áudio...";
  } else {
    falar("Gravação encerrada.");
    texto.textContent = "TEXTO............................";
  }
});

// Botão de câmera
cameraBtn.addEventListener("click", () => {
  falar("Abrindo câmera para captura de imagem.");
});

// Botão de ajuda
helpBtn.addEventListener("click", () => {
  falar("Este é um aplicativo de acessibilidade visual. Use os botões abaixo: câmera para capturar, microfone para gravar e este botão para ouvir ajuda.");
});

// Assistente de voz (lê o conteúdo da tela)
assistente.addEventListener("click", () => {
  const conteudo = `
    Localização: Avenida Paulista.
    Detalhes: Carros e prédios ao redor.
    O botão da esquerda abre a câmera.
    O botão do meio ativa o microfone.
    O botão da direita é de ajuda.
  `;
  falar(conteudo);
});

// Leitura inicial automática
window.onload = () => {
  falar("Aplicativo acessível carregado. Pronto para usar.");
};
