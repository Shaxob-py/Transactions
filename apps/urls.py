from django.urls import path

from apps.views import HomeListView, AddTransactionView, AuthRegisterFormView , LoginFormView

urlpatterns = [
    path('',HomeListView.as_view() , name='home'),
    path('register',AuthRegisterFormView.as_view() , name='register'),
    path('login', LoginFormView.as_view(), name='login'),
    path('add_transaction', AddTransactionView.as_view() , name='add_transaction'),

]
