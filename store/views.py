from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from django.contrib import messages

autenticado = False
# Create your views here.


def store(request):
    if testarAutenticado(request):
        clienteId = request.session['cliente']
        cliente = Cliente.objects.get(id=clienteId)
        ordem, created = Ordem.objects.get_or_create(
            cliente=cliente, completo=False)
        itens = ordem.ordemitem_set.all()
        carItens = ordem.get_car_itens
    else:
        # Create empty cart for now for non-logged in user
        items = []
        cliente = Cliente
        ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
        carItens = ordem['get_car_itens']

    produtos = Produto.objects.all()
    context = {'produtos': produtos,
               'carItens': carItens, 'autenticado': autenticado, 'cliente': cliente}
    return render(request, 'store/store.html', context)


def escolher(request):
    print('Aqui')
    return store(request)


def carrinho(request):
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem, created = Ordem.objects.get_or_create(
        cliente=cliente, completo=False)
    itens = ordem.ordemitem_set.all()
    carItens = ordem.get_car_itens
    if carItens != 0:
        context = {'items': itens, 'ordem': ordem, 'carItens': carItens}
        return render(request, 'store/cart.html', context)
    else:
        messages.erro(
            request, 'Sinto muito, mas você ainda não possui pedidos a finalizar!')

    produtos = Produto.objects.all()
    context = {'produtos': produtos,
               'carItens': carItens, 'autenticado': request.session['autenticado'], 'cliente': cliente}
    return render(request, 'store/store.html', context)


def checkout(request):
    if autenticado:
        clienteId = request.session['cliente']
        cliente = Cliente.objects.get(id=clienteId)
        ordem, created = Ordem.objects.get_or_create(
            cliente=cliente, completo=False)
        itens = ordem.orderitem_set.all()
        carItens = ordem.get_car_itens
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        carItens = order['get_cart_items']

    context = {'items': items, 'order': order, 'carItens': carItens}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produto']
    acao = data['acao']
    cliente = request.user.customer
    produto = Produto.objects.get(id=produtoId)
    ordem, created = Ordem.objects.get_or_create(
        cliente=cliente, completo=False)

    ordemItem, created = OrdemItem.objects.get_or_create(
        ordem=ordem, produto=produto)

    if acao == 'add':
        ordemItem.quantidade = (ordemItem.quantidade + 1)
    elif acao == 'remove':
        ordemItem.quantidade = (ordemItem.quantidade - 1)
    ordemItem.save()

    if ordemItem.quantity <= 0:
        ordemItem.delete()

    return JsonResponse('Item adcionado com sucesso', safe=False)


def entrar(request):
    return render(request, 'store/login.html')


def login(request):
    try:
        cliente = Cliente.objects.get(email=request.POST['email'])
        existe = True
    except:
        existe = False

    if existe and cliente.senha == request.POST['senha']:
        request.session['cliente'] = cliente.id
        clienteId = request.session['cliente']
        ordem, created = Ordem.objects.get_or_create(
            cliente=cliente, completo=False)
        itens = ordem.ordemitem_set.all()
        carItens = ordem.get_car_itens
        request.session['autenticado'] = True
        produtos = Produto.objects.all()
        context = {'produtos': produtos,
                   'carItens': carItens, 'autenticado': request.session['autenticado'], 'cliente': cliente}
        return render(request, 'store/store.html', context)
    else:
        items = []
        ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
        carItens = ordem['get_car_itens']
        request.session.clear
        if not existe:
            messages.error(request, 'E-mail não reconhecido!')
        else:
            messages.error(request, 'Senha está incorreta!')

        return render(request, 'store/login.html')


def sair(request):
    items = []
    cliente = Cliente
    ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
    carItens = ordem['get_car_itens']
    request.session.clear
    autenticado = False

    produtos = Produto.objects.all()
    context = {'produtos': produtos,
               'carItens': carItens, 'autenticado': autenticado, 'cliente': cliente}
    return render(request, 'store/store.html', context)


def testarAutenticado(request):
    try:
        autenticado = request.session['autenticado']
        return autenticado
    except:
        return False
