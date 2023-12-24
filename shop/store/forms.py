from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Customer, ShippingAddress,Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Логин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Подтвердить Пароль'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Логин'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Фамилия'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Почта'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Номер телефона'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Фамилия'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Адрес ул. дом. кв.'
            }),
            'city': forms.Select(attrs={
                'class': 'form_select contact__section-input',
                'placeholder': 'Выберите Город'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Регион'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form_control contact__section-input',
                'placeholder': 'Номер телефона'
            })
        }


class EditAccountFrom(UserChangeForm):
    old_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Пароль'
    }))
    new_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Подтвердить Пароль'
    }))
    confirm_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Подтвердить Пароль'
    }))
    username = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Логин'
    }))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Имя'
    }))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Фамилия'
    }))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Почта'
    }))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',  'old_password', 'new_password',
                  'confirm_password')




class EditProfileForm(forms.ModelForm):
    photo = forms.FileField(required=False,widget=forms.FileInput(attrs={
        'class': 'form-control contact__section-input'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input'
    }))
    class Meta:
        model = Profile
        fields = ['photo', 'phone_number']