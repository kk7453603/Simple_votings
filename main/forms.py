from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Такого адреса электронной почты не существует"
            self.add_error('email', msg)
        return email
