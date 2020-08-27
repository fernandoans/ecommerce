from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from django.contrib import messages

# Componentes da Loja
cliente = Cliente
ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
carItens = ordem['get_car_itens']


def store(request):
    try:
        autenticado = request.session['autenticado']
    except:
        autenticado = False

    if autenticado:
        clienteId = request.session['cliente']
        cliente = Cliente.objects.get(id=clienteId)
        ordem = Ordem.objects.get(cliente=cliente, completo=False)
        carItens = ordem.get_car_itens

    produtos = Produto.objects.all()
    context = {'produtos': produtos,
               'carItens': carItens, 'autenticado': autenticado, 'cliente': cliente}
    return render(request, 'store/store.html', context)


def add_item(request):
    # Dados do Formulário
    data = json.loads(request.body)
    produtoId = data['produtoId']
    # Dados Locais
    produto = Produto.objects.get(id=produtoId)
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem_qs = Ordem.objects.filter(cliente=cliente, completo=False)
    if ordem_qs.exists():
        ordem = ordem_qs[0]
    else:
        ordem = Ordem.objects.create(cliente=cliente, completo=False)
    itens = OrdemItem.objects.filter(ordem=ordem, produto=produto)
    if itens.exists():
        ordemItem = itens[0]
        ordemItem.quantidade = (ordemItem.quantidade + 1)
        ordemItem.save()
    else:
        ordemItem = OrdemItem.objects.create(
            produto=produto, ordem=ordem, quantidade=1)

    messages.success(request, produto.nome + ' foi adicionado com sucesso!')
    return JsonResponse('sucesso', safe=False)


def upd_item(request):
    # Dados do Formulário
    data = json.loads(request.body)
    produtoId = data['produtoId']
    acao = data['acao']
    # Dados Locais
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    produto = Produto.objects.get(id=produtoId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)
    # Localiza o Item
    itens = OrdemItem.objects.filter(ordem=ordem, produto=produto)
    # Dispara a ação
    for ordemItem in itens:
        if acao == 'add':
            ordemItem.quantidade = (ordemItem.quantidade + 1)
        elif acao == 'del':
            ordemItem.quantidade = (ordemItem.quantidade - 1)
        ordemItem.save()
        if ordemItem.quantidade <= 0:
            ordemItem.delete()

    return JsonResponse('sucesso', safe=False)


def carrinho(request):
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)
    carItens = ordem.get_car_itens
    if carItens != 0:
        itens = ordem.ordemitem_set.all()
        # Monta o Contexto e chama a tela
        context = {'carItens': carItens, 'ordem': ordem, 'itens': itens,
                   'autenticado': True, 'cliente': cliente}
        return render(request, 'store/cart.html', context)
    else:
        messages.error(request, 'Não existem pedidos a finalizar!')
        produtos = Produto.objects.all()
        # Monta o Contexto e chama a tela
        context = {'produtos': produtos,
                   'carItens': carItens, 'autenticado': True, 'cliente': cliente}
        return render(request, 'store/store.html', context)


def checkout(request):
    # Localiza os Dados
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)
    itens = ordem.ordemitem_set.all()
    carItens = ordem.get_car_itens
    # Monta o Contexto e chama a tela
    context = {'itens': itens, 'ordem': ordem,
               'carItens': carItens, 'cliente': cliente}
    return render(request, 'store/checkout.html', context)


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
    produtos = Produto.objects.all()
    context = {'produtos': produtos, 'carItens': carItens,
               'autenticado': False, 'cliente': cliente}
    return render(request, 'store/store.html', context)
