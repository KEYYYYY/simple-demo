from django.shortcuts import render
from django.views.generic.base import View

from users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {
            'login_form': login_form
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.save()
        return render(request, 'login.html', {
            'login_form': login_form
        })
