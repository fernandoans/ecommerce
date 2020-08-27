from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name='store'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('entrar/', views.entrar, name='entrar'),
    path('login/', views.login, name='login'),
    path('add-item/', views.add_item, name='add_item'),
    path('upd-item/', views.upd_item, name='upd_item'),
    path('sair/', views.sair, name='sair'),
]
