import nltk
import random
from datetime import datetime
from . import frases

nltk.data.path.append('/app/nltk_data')

PALAVRAS_POSITIVAS = {"feliz", "alegre", "bom", "ótimo", "excelente", "maravilhoso", "gostei", "legal", "animado", "tranquilo", "satisfeito"}
PALAVRAS_NEGATIVAS = {"triste", "chateado", "ruim", "péssimo", "horrível", "cansado", "irritado", "ansioso", "sofrendo", "desanimado", "decepcionado"}

EXPRESSOES_POSITIVAS = {
    "me senti bem", "dia maravilhoso", "tudo deu certo", "muito feliz", "fiquei animado",
    "dia produtivo", "estou em paz", "me diverti bastante", "tudo tranquilo",
    "recebi boas notícias", "consegui descansar", "trabalho reconhecido", "valeu a pena",
    "foi incrível", "cheio de gratidão", "só vitórias", "foi gratificante", "conquista importante",
    "recebi carinho", "me senti amado", "tempo com amigos", "abraços sinceros",
    "sorri muito", "tive tempo pra mim", "tudo fluiu bem", "me senti valorizado",
    "dia leve", "almocei com quem gosto", "estou com saúde", "sem preocupações",
    "fiz algo bom", "ajudei alguém", "boas lembranças", "experiência positiva",
    "consegui realizar", "tudo correu bem", "orgulho de mim", "metas alcançadas",
    "emocionante no bom sentido", "fui elogiado", "me senti útil", "pude descansar",
    "voltei a sorrir", "tive bons momentos", "recebi apoio", "tive esperança",
    "dia feliz", "senti paz interior", "dia de superação", "curti bastante",
    "me senti renovado", "vivi intensamente", "me senti motivado", "consegui resolver tudo",
    "dia excelente", "recebi incentivo", "tive fé", "tive paciência", "tudo fez sentido",
    "reconhecimento merecido", "me senti especial", "tempo de qualidade", "fiquei em boa companhia",
    "me senti forte", "tudo se encaixou", "me senti seguro", "fui compreendido",
    "resolvi pendências", "melhorei bastante", "tive uma conquista", "revi alguém querido",
    "foi tudo ótimo", "gratidão define", "me senti leve", "me senti acolhido",
    "trouxe alegria", "foi divertido", "me recuperei bem", "estou bem comigo mesmo",
    "me senti esperançoso", "consegui ajudar", "me senti em casa", "fiz o meu melhor",
    "coisas boas aconteceram", "tive sorte", "pessoas boas por perto", "energia positiva",
    "me senti em paz", "dia de vitórias", "realizações importantes", "momento especial",
    "estou no caminho certo", "sensação boa", "cresci como pessoa", "vibrações positivas",
    "dia inspirador", "repleto de amor", "tempo bem aproveitado", "satisfação total"
}

EXPRESSOES_NEGATIVAS = {
    "me senti mal", "dia horrível", "tudo deu errado", "muito triste", "fiquei irritado",
    "dia improdutivo", "me senti sozinho", "me estressei", "tudo confuso", "recebi más notícias",
    "não consegui descansar", "trabalho ignorado", "não valeu a pena", "foi terrível",
    "cheio de raiva", "só derrotas", "foi frustrante", "perdi algo importante",
    "me senti rejeitado", "tempo desperdiçado", "discussões em casa", "chorei bastante",
    "me senti usado", "tudo desandou", "não fui ouvido", "dia pesado", "almocei sozinho",
    "não estou bem", "cheio de preocupações", "fiz algo ruim", "magoado com alguém",
    "más lembranças", "experiência negativa", "fui ignorado", "não consegui nada",
    "senti vergonha", "sem forças", "emocional abalado", "me senti inútil", "não pude descansar",
    "me senti vazio", "tive maus momentos", "falta de apoio", "sem esperança", "dia péssimo",
    "ansiedade constante", "fui julgado", "fiquei nervoso", "sem motivação", "me senti fraco",
    "nada deu certo", "fui mal interpretado", "não consegui lidar", "foi um desastre",
    "fui criticado", "me senti excluído", "tudo muito difícil", "descontrole emocional",
    "problemas de saúde", "sem direção", "fiquei decepcionado", "fui traído",
    "não fui valorizado", "tempo perdido", "briguei com alguém", "fiquei confuso",
    "culpa por tudo", "me senti pressionado", "me senti abandonado", "falta de sentido",
    "desânimo total", "frustração constante", "nada mudou", "dias difíceis",
    "me senti incapaz", "dores emocionais", "pensamentos ruins", "desejo de sumir",
    "preocupações demais", "sem perspectivas", "sem carinho", "isolado de todos",
    "desesperança", "só tristeza", "coração apertado", "tudo desmoronando",
    "sentimento de fracasso", "dia sem cor", "sem amor", "falta de controle",
    "só coisas ruins", "ninguém me entende", "me senti pequeno", "rejeição total",
    "falta de apoio", "quebrado por dentro", "estou me arrastando", "vontade de chorar"
}

def obter_dia_semana():
    dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
            "sexta-feira", "sábado", "domingo"]
    return dias[datetime.now().weekday()]

def analisar_sentimento_palavras(texto):
    texto_lower = texto.lower()
    score = 0

    # Verifica expressões compostas primeiro
    for expressao in EXPRESSOES_POSITIVAS:
        if expressao in texto_lower:
            score += 2
    for expressao in EXPRESSOES_NEGATIVAS:
        if expressao in texto_lower:
            score -= 2

    # Tokeniza para contagem de palavras individuais
    palavras = nltk.word_tokenize(texto_lower)
    positivos = sum(1 for p in palavras if p in PALAVRAS_POSITIVAS)
    negativos = sum(1 for p in palavras if p in PALAVRAS_NEGATIVAS)
    score += positivos - negativos

    if score > 0:
        return 1  # positivo
    elif score < 0:
        return -1  # negativo
    else:
        return 0  # neutro

def gerar_frase(sentimento, dia_semana, nome_usuario=""):
    if sentimento == "positivo":
        frase = random.choice(frases.frases_positivo)
        atividade = random.choice(frases.atividade_recomendada["positivo"])
    elif sentimento == "negativo":
        frase = random.choice(frases.frases_negativo)
        atividade = random.choice(frases.atividade_recomendada["negativo"])
    else:
        frase = random.choice(frases.frases_neutro)
        atividade = random.choice(frases.atividade_recomendada["neutro"])

    frase = frase.replace("{dia_semana}", dia_semana)
    frase = frase.replace("{nome_usuario}", nome_usuario)
    frase = frase.replace("{atividade_recomendada}", atividade)

    return frase

def analisar_postagens(postagens, nome_usuario=""):
    if not postagens:
        return "neutro", "Nenhuma postagem para analisar hoje."

    pontuacoes = [analisar_sentimento_palavras(texto) for texto in postagens]  # usa textos, não postagens
    media = sum(pontuacoes) / len(pontuacoes)

    if media > 0.3:
        sentimento = "positivo"
    elif media < -0.3:
        sentimento = "negativo"
    else:
        sentimento = "neutro"

    dia_semana = obter_dia_semana()
    frase = gerar_frase(sentimento, dia_semana, nome_usuario)

    return sentimento, frase
