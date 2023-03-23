from django.shortcuts import render

from django.views.generic import CreateView

from django.urls import reverse_lazy

from .froms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')  # login - параметр name функции path
    template_name = 'signup.html'
