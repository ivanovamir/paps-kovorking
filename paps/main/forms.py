from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=25)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Логин")
        self.fields['password'].label = _("Пароль")


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
        'password_too_short': _("Пароль слишком короткий. Он должен содержать не менее 8 символов."),
        'password_common': _("Пароль слишком распространенный."),
        'password_numeric': _("Пароль полностью состоит из цифр."),
        'username': {
            'unique': _("Пользователь с таким именем уже существует."),
        },
        # Добавьте другие переводы по мере необходимости
    }

    class Meta:
        model = User
        fields = ('username', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Логин")
        self.fields['password1'].label = _("Пароль")
