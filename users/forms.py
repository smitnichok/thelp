from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from empl.models import Category
from users.models import Adresses, User, Post


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="логин",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    adress = forms.ModelChoiceField(queryset=Adresses.objects.all(), empty_label="Адрес магазина/офиса", label="адрес")
    post = forms.ModelChoiceField(queryset=Post.objects.all(), empty_label="Должность", label="Должность")

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2', 'number_phone', 'post',
                  'cabinet', 'adress']
        labels = {
            'email': 'E-mail',
            'first_name': "имя",
            'last_name': "фамилия",
            'patronymic': 'отчество',
            'number_phone': 'номер телефона',
            'post': 'должность',
            'cabinet': '№ кабинета',
            'adress': 'адрес',
            'image': 'фото'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'number_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'cabinet': forms.NumberInput(attrs={'class': 'form-input'}),

        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    adress = forms.ModelChoiceField(queryset=Adresses.objects.all(), empty_label="Адрес магазина/офиса", label="Место работы",
                                    widget=forms.Select(attrs={'class': 'custom-dropdown'}))
    post = forms.ModelChoiceField(queryset=Post.objects.all(), empty_label="Должность", label="Должность",
                                  widget=forms.Select(attrs={'class': 'custom-dropdown'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username','patronymic',  'email', 'number_phone', 'cabinet', 'adress']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'отчество',
            'number_phone': 'номер телефона',
            'cabinet': '№ кабинета',
            'adress': 'адрес',

        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'patronymic': forms.TextInput(attrs={'class': 'input-field'}),
            'number_phone': forms.TextInput(attrs={'class': 'input-field'}),



        }
