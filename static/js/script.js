let chat = document.querySelector('#chat');
chat.addEventListener('submit', function (event) {
    event.preventDefault();
});
let textInput = document.querySelector('#textInput');
let botaoEnviar = document.querySelector('#botao-enviar');

let arquivoSelecionado;
let botaoAnexo = document.querySelector("#input-arquivo");
let miniaturaArquivo;

async function pegarArquivo() {
    let fileInput = document.createElement("input");
    fileInput.type = 'file';
    fileInput.accept = '.txt,.pdf';

    fileInput.onchange = async e => {
        if (miniaturaArquivo) {
            miniaturaArquivo.remove();
        }

        arquivoSelecionado = e.target.files[0];
        miniaturaArquivo = document.createElement('img');
        miniaturaArquivo.src = URL.createObjectURL(arquivoSelecionado);
        miniaturaArquivo.style.maxWidth = '3rem';
        miniaturaArquivo.style.maxHeight = '3rem';
        miniaturaArquivo.style.margin = '0.5rem';
        // Adicione a miniatura ao container do formulário
        let container = document.querySelector('.container');
        if (container) container.appendChild(miniaturaArquivo);

        let formData = new FormData();
        formData.append('file', arquivoSelecionado);

        const response = await fetch('http://127.0.0.1:5000/Upload_file', {
            method: 'POST',
            body: formData
        });

        const resposta = await response.text();
        console.log(resposta);
        console.log(arquivoSelecionado);
    }
    fileInput.click();
}

async function enviar_mensagem() {
    if (textInput.value == "" || textInput.value == null) return;
    let mensagem = textInput.value;
    if (miniaturaArquivo) {
        miniaturaArquivo.remove();
    }

    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando"

    let estados = ["Analisando .", "Analisando ..", "Analisando ...", "Analisando ."]
    let indiceEstado = 0;

    let intervaloAnimacao = setInterval(() => {
        novaBolhaBot.innerHTML = estados[indiceEstado];
        indiceEstado = (indiceEstado + 1) % estados.length;
    }, 500);


    // Envia requisição com a mensagem para a API do ChatBot
    const resposta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 'msg': mensagem }),
    });
    let dados;
    try {
        dados = await resposta.json();
    } catch (e) {
        // Se não for JSON, não tente ler novamente o corpo!
        dados = { categoria: '', resposta: 'Erro ao processar resposta do servidor.' };
    }
    console.log(dados);

    clearInterval(intervaloAnimacao);

    novaBolhaBot.innerHTML = (dados.resposta || '').replace(/\n/g, '<br>');
    vaiParaFinalDoChat();

    // Atualiza os campos de resultado
    document.getElementById('categoria').textContent = dados.categoria || '';
    document.getElementById('resposta').textContent = dados.resposta || '';
}
function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', function (event) {
    event.preventDefault();
    enviar_mensagem();
});
textInput.addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

botaoAnexo.addEventListener('click', pegarArquivo);