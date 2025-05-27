// Formatação do número de telefone
Inputmask({"mask": "(99) 99999-9999"}).mask(document.querySelector('[name="telefone"]'));

let currentStep = 1;
const steps = document.querySelectorAll('.form-md-container');
const nextBtns = document.querySelectorAll('.next-btn');
const prevBtns = document.querySelectorAll('.prev-btn');

// Mostrar o próximo passo
nextBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        if (currentStep < steps.length) {
            steps[currentStep - 1].style.display = 'none';
            steps[currentStep].style.display = 'block';
        currentStep++;
        }
    });
});

// Voltar para o passo anterior
prevBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      if (currentStep > 1) {
        steps[currentStep - 1].style.display = 'none';
        steps[currentStep - 2].style.display = 'block';
        currentStep--;
      }
    });
});

const campoNome = document.getElementById("id_nome_completo");
const campoData = document.getElementById("id_data_nascimento");
const campoEmail = document.getElementById("id_email");
const campoSenha = document.getElementById("id_password1");
const campoConfirma = document.getElementById("id_password2");

function verificaCampo() { // Verifica se os campos obrigatórios estão preenchidos
    if (currentStep === 1) {
        if (campoNome.value.trim() !== '' && campoData.value !== '') {
          document.getElementById("proximo_1").disabled = false;
        } else {
          document.getElementById("proximo_1").disabled = true;
        }
    }
    if (currentStep === 2) {
        if (campoEmail.value === "" && campoSenha !== "" && campoConfirma !== "") {  // Verifica se email e senha está preenchido
            document.getElementById("botao_cadastro").disabled = false;
        } else {
            document.getElementById("botao_cadastro").disabled = true;
        }
    }
}
    
campoNome.addEventListener('input', verificaCampo);
campoData.addEventListener('input', verificaCampo);
campoEmail.addEventListener('input', verificaCampo);
campoSenha.addEventListener('input', verificaCampo);
campoConfirma.addEventListener('input', verificaCampo);

function previewImage(event) {
    const input = event.target;
    const preview = document.getElementById('preview');
    const removeBtn = document.getElementById('removeImageBtn');
    const maxSize = 2 * 1024 * 1024; // 2MB

    if (input.files && input.files[0]) {
        const file = input.files[0];

        // Verifica o tamanho da imagem
        if (file.size > maxSize) {
            alert("A imagem não pode ter mais que 2MB.");
            input.value = "";
            preview.style.display = 'none';
            removeBtn.style.display = 'none';
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            removeBtn.style.display = 'inline-block';
        }
        reader.readAsDataURL(file);
    }
}

function removeImage() { // Remove a imagem selecionada para o perfil
    const input = document.querySelector('input[type="file"]');
    const preview = document.getElementById('preview');
    const removeBtn = document.getElementById('removeImageBtn');
    
    input.value = '';  // Limpa o campo de arquivo
    preview.src = '#';
    preview.style.display = 'none';
    removeBtn.style.display = 'none';
}

// Força da senha
const verificaSenha = document.querySelector('[name="password1"]');
verificaSenha.addEventListener('input', function () {
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    let senha = verificaSenha.value;
    let forca = 0;
    let strength = '';
    let width = '0%';

    // Verifica se a senha tem pelo menos 8 caracteres
    if (senha.length >= 8) {
        forca += 1;
    }
    // Verifica se a senha contém letras maiúsculas
    if (/[A-Z]/.test(senha)) {
        forca += 1;
    }
    // Verifica se a senha contém letras minúsculas
    if (/[a-z]/.test(senha)) {
        forca += 1;
    }
    // Verifica se a senha contém números
    if (/\d/.test(senha)) {
        forca += 1;
    }
    // Verifica se a senha contém caracteres especiais
    if (/[\W_]/.test(senha)) {
        forca += 1;
    }

    // Definir a força da senha
    if (forca <= 1) {
        strength = 'Muito Fraca';
        width = '10%';
    } else if (forca === 2) {
        strength = 'Fraca';
        width = '30%';
    } else if (forca === 3) {
        strength = 'Média';
        width = '60%';
    } else if (forca === 4) {
        strength = 'Forte';
        width = '80%';
    } else if (forca === 5) {
        strength = 'Muito Forte';
        width = '100%';
    }
    strengthText.textContent = `Força da senha: ${strength}`;
    strengthBar.style.width = width;
});

const senha1 = document.getElementById("id_password1");
const senha2 = document.getElementById("id_password2");
function compararSenha () {
    const paragrafo = document.getElementById("compara_senha");
    if (senha1.value !== '' && senha1.value === senha2.value) {
        paragrafo.innerText = "As senhas são iguais";
        paragrafo.style.color = "green";
        paragrafo.style.fontWeight = "bold";
        document.getElementById("botao_cadastro").disabled = false;
    } else {
        paragrafo.innerText = "As senhas são diferentes";
        paragrafo.style.color = "red";
        paragrafo.style.fontWeight = "bold";
        document.getElementById("botao_cadastro").disabled = true;
    }
}
  
senha1.addEventListener('input', compararSenha);
senha2.addEventListener('input', compararSenha);

function verificarTamanho(input) {
    const maxSize = 2 * 1024 * 1024; // 2MB
    if (input.files[0].size > maxSize) {
        alert("A imagem excede o tamanho máximo de 2MB.");
        input.value = "";
    }
}