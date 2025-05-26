from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Postagem
from .forms import PostagemForm, CustomUserCreationForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from datetime import timedelta
from django.utils.timezone import now
from datetime import time, datetime
from accounts.analise import analisar_postagens
from collections import defaultdict, Counter
from datetime import datetime
from accounts import analise

def inicio_view(request):
    return render(request, 'index.html')

def ajuda_view(request):
    return render(request, 'ajuda.html')

def sobre_view(request):
    return render(request, 'sobre.html')

def service_worker(request):
    js = render_to_string('service-worker.js')
    return HttpResponse(js, content_type='application/javascript')

def login_view(request):
    if request.method == 'POST':
        # Recebe os dados do formulário
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Autentica o usuário
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)  # Realiza o login do usuário
            return redirect('perfil')  # Redireciona para a página de perfil
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')  # Retorna para a página de login

    return render(request, 'login.html')

# Página de perfil protegida
@login_required
def perfil(request):
    return render(request, 'perfil.html', {
        'usuario': request.user  # Passa o usuário logado para a template
    })


def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'cadastro.html', {'form': form})

@login_required
def diario(request):
    usuario = request.user
    data_str = request.GET.get('criado_em')

    if data_str:
        data_formatada = parse_date(data_str)  # converte string para date
        if data_formatada:
            inicio_do_dia = datetime.combine(data_formatada, time.min)
            fim_do_dia = datetime.combine(data_formatada, time.max)
            postagens = Postagem.objects.filter(usuario=usuario, criado_em__range=(inicio_do_dia, fim_do_dia))
        else:
            postagens = Postagem.objects.filter(usuario=usuario)
    else:
        postagens = Postagem.objects.filter(usuario=usuario)

    # extrair textos para análise
    textos = [p.texto for p in postagens]
    analise_hoje = analisar_postagens(textos, nome_usuario=usuario.get_full_name())

    # resto da view...
    return render(request, 'diario.html', {
        'usuario': usuario,
        'postagens': postagens,
        'analise_hoje': analise_hoje
    })

@login_required
def nova_postagem(request):
    if request.method == 'POST':
        form = PostagemForm(request.POST)
        if form.is_valid():
            postagem = form.save(commit=False)
            postagem.usuario = request.user

            # Garante que a data foi enviada e converte
            if postagem.criado_em:
                data_formatada = parse_date(str(postagem.data))
                postagem.dia_semana = data_formatada.strftime('%A')  # Ex: 'sábado'

            postagem.save()
            return redirect('perfil_diario')
    else:
        form = PostagemForm()
    return render(request, 'nova_postagem.html', {'form': form})

@login_required
def perfil_editar(request):
    usuario = request.user

    if request.method == 'POST':
        usuario.nome_completo = request.POST.get('nome_completo')
        usuario.data_nascimento = request.POST.get('data_nascimento')
        usuario.telefone = request.POST.get('telefone')
        usuario.bio_perfil = request.POST.get('bio_perfil')

        # Remover foto
        if request.POST.get('remover_foto') == 'true':
            if usuario.foto_perfil:
                usuario.foto_perfil.delete(save=False)
            usuario.foto_perfil = None

        # Substituir foto nova
        elif 'foto_perfil' in request.FILES:
            usuario.foto_perfil = request.FILES['foto_perfil']

        try:
            usuario.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao salvar: {e}')

        return redirect('perfil')

    return render(request, 'perfil_editar.html', {'usuario': usuario})

@login_required
def excluir_conta(request):
    if request.method == 'POST':
        senha = request.POST.get('senha_confirmacao')
        if not check_password(senha, request.user.password):
            messages.error(request, 'Senha incorreta. Conta não excluída.')
            return redirect('perfil_editar')
        
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('login')
    return redirect('perfil')

@login_required
def visualizar_postagem(request, postagem_id):
    postagem = get_object_or_404(Postagem, id=postagem_id, usuario=request.user)

    return render(request, 'visualizar_postagem.html', {
        'postagem': postagem
    })
    
@login_required
def excluir_postagem(request, postagem_id):
    postagem = get_object_or_404(Postagem, id=postagem_id, usuario=request.user)

    if request.method == 'POST':
        postagem.delete()
        return redirect('perfil_diario')

    return redirect('visualizar_postagem', postagem_id=postagem.id)

def relatorio_analise(request):
    usuario = request.user
    periodo_str = request.GET.get("periodo", "30")

    try:
        periodo = int(periodo_str)
        if periodo <= 0:
            periodo = 30
    except ValueError:
        periodo = 30

    data_limite = datetime.now() - timedelta(days=periodo)

    if not usuario.is_authenticated:
        return redirect('login')

    postagens = Postagem.objects.filter(usuario=usuario, criado_em__gte=data_limite)

    nome_usuario = getattr(usuario, 'nome_completo', None)
    if not nome_usuario:
        nome_usuario = usuario.username if hasattr(usuario, 'username') else 'Usuário'

    relatorio = gerar_relatorio_emocional(postagens, nome_usuario=nome_usuario)

    contexto = {
    "usuario": usuario,
    "periodo": periodo,
    "data_atual": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "dados_grafico": relatorio["dados_grafico"],
    "mais_frequente": relatorio["mais_frequente"],
    "frases_dia_semana": relatorio["frases_dia_semana"],
    "analise_por_dia": relatorio["analise_por_dia"],
     "frases_semana": relatorio["frases_semana"]
    
}
    return render(request, "relatorios.html", contexto)

dias_semana_pt = {
    'monday': 'segunda-feira',
    'tuesday': 'terça-feira',
    'wednesday': 'quarta-feira',
    'thursday': 'quinta-feira',
    'friday': 'sexta-feira',
    'saturday': 'sábado',
    'sunday': 'domingo'
}

def nome_dia_semana(dt):
    dia_en = dt.strftime('%A').lower()
    return dias_semana_pt.get(dia_en, dia_en)

# Função principal: gera relatório emocional

def gerar_relatorio_emocional(postagens, nome_usuario=""):
    if not postagens:
        return {
            "dados_grafico": {"positivo": 0, "negativo": 0, "neutro": 0},
            "mais_frequente": "neutro",
            "frases_dia_semana": ["Nenhuma postagem encontrada no período selecionado."],
            "analise_por_dia": []
        }

    contagem_sentimento = Counter()
    postagens_por_dia = defaultdict(list)

    for postagem in postagens:
        postagens_por_dia[postagem.dia_semana].append(postagem)
        contagem_sentimento[postagem.emocao_tipo] += 1

    # Mapeia números para nomes legíveis
    EMOCAO_MAP = {
        1: "positivo",
        2: "negativo",
        3: "neutro"
    }

    mais_frequente_valor = contagem_sentimento.most_common(1)[0][0]
    mais_frequente = EMOCAO_MAP.get(mais_frequente_valor, "neutro")

    frases_dia_semana = []
    analise_por_dia = []
    frases_semana = gerar_frases_sentimentos_por_dia(postagens)

    for dia, lista_postagens in sorted(postagens_por_dia.items()):
        total = len(lista_postagens)
        positivas = sum(1 for p in lista_postagens if p.emocao_tipo == 1)
        negativas = sum(1 for p in lista_postagens if p.emocao_tipo == 2)
        neutras = sum(1 for p in lista_postagens if p.emocao_tipo == 3)

        frase = f"No {dia.lower()}, foram feitas {total} postagens: {positivas} positivas, {negativas} negativas e {neutras} neutras."
        frases_dia_semana.append(frase)

        analise_por_dia.append({
            "dia": dia,
            "total_postagens": total,
            "positivo": positivas,
            "negativo": negativas,
            "neutro": neutras,
        })

    dados_grafico = {
        "positivo": contagem_sentimento.get(1, 0),
        "negativo": contagem_sentimento.get(2, 0),
        "neutro": contagem_sentimento.get(3, 0),
    }

    return {
        "dados_grafico": dados_grafico,
        "mais_frequente": mais_frequente,
        "frases_dia_semana": frases_dia_semana,
        "analise_por_dia": analise_por_dia,
        "frases_semana" : frases_semana
    }
    
def gerar_frases_sentimentos_por_dia(postagens):
    if not postagens:
        return ["Nenhuma frase gerada."]

    dias_da_semana = {
        0: "Nas segundas-feiras",
        1: "Nas terças-feiras",
        2: "Nas quartas-feiras",
        3: "Nas quintas-feiras",
        4: "Nas sextas-feiras",
        5: "Nos sábados",
        6: "Nos domingos"
    }

    EMOCAO_MAP = {
        1: "feliz",
        2: "triste",
        3: "neutro"
    }

    # Agrupa postagens por dia da semana
    postagens_por_dia = defaultdict(list)
    for postagem in postagens:
        dia_semana = postagem.criado_em.weekday()  # 0 = segunda, 6 = domingo
        postagens_por_dia[dia_semana].append(postagem)

    frases = []
    for dia_int in sorted(postagens_por_dia.keys()):
        lista = postagens_por_dia[dia_int]
        if not lista:
            continue

        contagem = Counter(p.emocao_tipo for p in lista)
        emocao_predominante = contagem.most_common(1)[0][0]
        nome_emocao = EMOCAO_MAP.get(emocao_predominante, "neutro")
        nome_dia = dias_da_semana[dia_int]

        frases.append(f"{nome_dia}, você se sentiu mais {nome_emocao}.")

    return frases