from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Challenge
from django import forms


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('challenges')


class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('challenges')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('challenges')
        return super().get(request, *args, **kwargs)

class CreateChallengeView(LoginRequiredMixin, CreateView):
    model = Challenge
    template_name = 'app/create_challenge.html'
    fields = ['player', 'title', 'description']

    def form_valid(self, form):
        print("Challenger:", self.request.user)
        form.instance.challenger = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('challenges')

class PendingChallengesView(LoginRequiredMixin, ListView):
    model = Challenge
    template_name = 'app/pending_challenges.html'
    context_object_name = 'pending_challenges'

    def get_queryset(self):
        return Challenge.objects.filter(player=self.request.user, accepted=False)

class AcceptChallengeView(LoginRequiredMixin, DeleteView):
    model = Challenge
    template_name = 'app/accept_challenge.html'
    success_url = '/challenges/'

    def get_queryset(self):
        return Challenge.objects.filter(player=self.request.user, accepted=False)

class ChallengesView(LoginRequiredMixin, ListView):
    model = Challenge
    template_name = 'app/challenges.html'
    context_object_name = 'challenges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_challenges'] = Challenge.objects.filter(player=self.request.user, accepted=True)
        context['challenger_challenges'] = Challenge.objects.filter(challenger=self.request.user, accepted=True)
        return context
    
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))

