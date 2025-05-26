# Importação das bibliotecas necessárias
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Postagem
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Colocando o objeto Usuário em uma variável
User = get_user_model()

# Formulário de cadastro
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'

    class Meta:
        model = CustomUser
        fields = [
            'nome_completo',
            'email',
            'password1',
            'password2',
        ]
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva seu nome completo', 'maxlength': '50'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu email'
            }),
        }

    # Verifica se o email já está sendo usado
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    # Salva o novo cadastro
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

# Formulário de postagem
class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'texto', 'emocao_tipo', 'emoji', 'intensidade']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '560'}),
            'emoji': forms.Select(attrs={'class': 'form-select'}),
        }

# Formulário do perfil
class PerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'nome_completo',
            'data_nascimento',
            'foto_perfil',
            'bio_perfil',
            'telefone',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

# Verifica o tamanho da imagem antes de carregar
def clean_foto_perfil(self):
        imagem = self.cleaned_data.get('foto_perfil')
        if imagem and imagem.size > 2 * 1024 * 1024:
            raise forms.ValidationError('A imagem deve ter no máximo 2MB.')
        return imagem
