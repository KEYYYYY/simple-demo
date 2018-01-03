from django.forms import ModelForm

from users.models import UserProfile


class LoginForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'identity']
