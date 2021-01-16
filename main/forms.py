from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()
