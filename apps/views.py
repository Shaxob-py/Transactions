from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from apps.form import AddTransactionModelForm, AuthRegisterMoelForm, LoginModelForm
from apps.models import Transaction


class AuthRegisterFormView(FormView):
    template_name = 'app/auth/register.html'
    success_url = reverse_lazy('home')
    form_class = AuthRegisterMoelForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     for error in form.errors.values():
    #         messages.error(self.request, error)
    #     return super().form_invalid(form)
    def form_invalid(self, form):
        print("Xatolik:", form.errors)
        return super().form_invalid(form)

class HomeListView(ListView):
    model = Transaction
    template_name = 'app/home.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        transactions = Transaction.objects.all()

        total_income = transactions.filter(type='income').aggregate(Sum('total_balance'))['total_balance__sum'] or 0
        total_expenses = transactions.filter(type='expense').aggregate(Sum('total_balance'))['total_balance__sum'] or 0
        total_balance = total_income - total_expenses

        data['total_transactions'] = transactions.count()
        data['total_income'] = total_income
        data['total_expenses'] = total_expenses
        data['total_balance'] = total_balance
        data['transactions'] = Transaction.objects.all()

        return data


class AddTransactionView(FormView):
    template_name = 'app/add_transaction.html'
    success_url = reverse_lazy('home')
    form_class = AddTransactionModelForm

    def form_valid(self, form ):
        user = request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Xatolik:", form.errors)
        return super().form_invalid(form)

class LoginFormView(FormView):
    template_name = 'app/auth/login.html'
    success_url = reverse_lazy('home')
    form_class = LoginModelForm

    def form_valid(self, form):
        login(self.request , form.user)

        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)