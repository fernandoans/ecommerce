from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name='store'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('entrar/', views.entrar, name='entrar'),
    path('login/', views.login, name='login'),
    path('', views.escolher, name='escolher'),
    path('', views.sair, name='sair'),
]
