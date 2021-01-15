from django_registration.forms import RegistrationForm
from main.models import User


class UserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
