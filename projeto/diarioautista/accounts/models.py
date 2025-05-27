# Importação das bibliotecas necessárias
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Verifica o tamanho da imagem antes de salvar
def validar_tamanho_imagem(imagem):
    limite_mb = 2  # tamanho máximo em megabytes
    if imagem.size > limite_mb * 1024 * 1024:
        raise ValidationError(f'A imagem não pode ter mais que {limite_mb}MB.')

# Modelo de usuário customizado
class CustomUser(AbstractUser):
    username = None  # Desativa o campo username
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', 
        null=True, 
        blank=True, 
        validators=[validar_tamanho_imagem]
    )
    bio_perfil = models.CharField(max_length=140, null=True, blank=True, default="Ainda não escreveu uma bio.")
    telefone = models.CharField(max_length=20, null=True, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'data_nascimento']

    def __str__(self):
        return self.email

# Modelo de postagem
class Postagem(models.Model):
    
    User = get_user_model()
    
    EMOCAO_CHOICES = [
        (1, 'Positiva'),
        (2, 'Negativa'),
        (3, 'Neutro'),
    ]

    EMOJI_CHOICES = [
        (1, '😊 Feliz'),
        (2, '😢 Triste'),
        (3, '😡 Bravo'),
        (4, '😱 Assustado'),
        (5, '😴 Cansado'),
        (6, '🤗 Acolhido'),
        (7, '😤 Frustrado'),
        (8, '😍 Apaixonado'),
        (9, '🤯 Sobrecarregado'),
        (10, '😐 Neutro'),
        (11, '😕 Confuso'),
        (12, '🤩 Animado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='postagens'
    )
    titulo = models.CharField(max_length=100, blank=True, null=True)
    texto = models.TextField()
    emocao_tipo = models.IntegerField(choices=EMOCAO_CHOICES)
    emoji = models.IntegerField(choices=EMOJI_CHOICES)
    intensidade = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    dia_semana = models.CharField(max_length=15, blank=True, editable=False)

    # Salva a postagem
    def save(self, *args, **kwargs):
        # Garante que criado_em esteja definido antes de calcular dia_semana
        if not self.criado_em:
            self.criado_em = timezone.now()
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        self.dia_semana = dias[self.criado_em.weekday()]
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.titulo or "Postagem sem título"} - {self.criado_em.date()} ({self.dia_semana})'
