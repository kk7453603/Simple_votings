from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()


class ProfileEditingForm(forms.Form):
    username = forms.CharField(
        label='Редактировать имя пользователя:',
        max_length=150,
        required=True,
    )
    first_name = forms.CharField(label='Редактировать имя:', max_length=150, required=False)
    last_name = forms.CharField(label='Редактировать фамилию:', max_length=150, required=False)
    email = forms.EmailField(label='Редактировать email:', required=True)


class VotingForm(forms.Form):
    radio_variant = forms.ChoiceField(widget=forms.RadioSelect)
    checkbox_variant = forms.ChoiceField(widget=forms.CheckboxSelectMultiple)


class PasswordEditingForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Старый пароль', 'class': 'form-control'}
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Новый пароль', 'class': 'form-control'}
        )
    )
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Повторите новый пароль', 'class': 'form-control'}
        )
    )
