// Configuração inicial
const body = document.body;
const btnTema = document.getElementById("btn-tema");
const btnAumentarFonte = document.getElementById("btn-aumentar-fonte");
const btnDiminuirFonte = document.getElementById("btn-diminuir-fonte");

// Valores de fonte em "em"
let fonteAtual = 1.0;
const fonteMin = 0.8;
const fonteMax = 1.6;
const passoFonte = 0.1;

// Alterna entre tema claro e escuro
function alternarTema() {
    body.classList.toggle("tema-escuro");
    const temaAtual = body.classList.contains("tema-escuro") ? "escuro" : "claro";
    localStorage.setItem("tema", temaAtual);
}

// Aumenta o tamanho da fonte
function aumentarFonte() {
    if (fonteAtual < fonteMax) {
        fonteAtual = parseFloat((fonteAtual + passoFonte).toFixed(1));
        aplicarFonte();
    }
}

// Diminui o tamanho da fonte
function diminuirFonte() {
    if (fonteAtual > fonteMin) {
        fonteAtual = parseFloat((fonteAtual - passoFonte).toFixed(1));
        aplicarFonte();
    }
}

// Aplica o tamanho da fonte ao body e salva no localStorage
function aplicarFonte() {
    body.style.fontSize = fonteAtual + "em";
    localStorage.setItem("fonte", fonteAtual.toString());
}

// Aplica as preferências salvas (tema e fonte)
function aplicarPreferenciasSalvas() {
    const temaSalvo = localStorage.getItem("tema");
    const fonteSalva = localStorage.getItem("fonte");

    if (temaSalvo === "escuro") {
        body.classList.add("tema-escuro");
    }

    if (fonteSalva) {
        const fonteConvertida = parseFloat(fonteSalva);
        if (!isNaN(fonteConvertida)) {
            fonteAtual = fonteConvertida;
            aplicarFonte();
        }
    }
}

// Eventos
btnTema?.addEventListener("click", alternarTema);
btnAumentarFonte?.addEventListener("click", aumentarFonte);
btnDiminuirFonte?.addEventListener("click", diminuirFonte);

window.addEventListener("DOMContentLoaded", aplicarPreferenciasSalvas);
