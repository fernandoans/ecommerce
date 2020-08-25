# eCommerce
Este é um projeto Open Source completo para um Site eCommerce em Django (ainda em produção). O objetivo é um modelo de concepção para uma loja virtual (que pode ser para a venda de qualquer produto) com a utilização dos seguintes softwares:
* Django - Versão 3.1
* Bootstrap (futuramente será modificado para o Material) para responsividade das telas
* JavaScript e CSS3

## Escopo do Projeto
Este eCommerce é uma Padaria Virtual construída com o Django, a tela inicial mostra a "vitrine" de produtos disponíveis:

![Tela Inicial](doc/01-Inicial.png)

Para comprar o cliente deve realizar um registro e acessar o site (todo o controle é realizado pelo Administrador):

![Tela Login](doc/02-Login.png)

![Tela Inicial](doc/03-Logado.png)

Uma vez escolhidos os produtos o cliente pode entrar no seu carrinho para escolher as quantidades, ou remover os produtos selecionados:

![Tela do Carrinho](doc/04-Carrinho.png)

Uma vez definido os produtos e a quantidade, o cliente pode proceder o pagamento:

![Tela do Pagamento](doc/05-Pagamento.png)

## Vantagens no uso do Django
Não existe a necessidade de se criar telas administrativas para cadastro e manutenção dos produtos e clientes, tudo é realizado pelo administrador do Django:

![Tela Administrativa](doc/06-Administracao.png)

## Situação do Projeto

Este projeto ainda está em desenvolvimento, atualmente está pronto e funcional:
* Definição do modelo de dados
* Concepção das telas com responsividade
* Tela Inicial
* Login e Logout
* Bloqueio de compra para clientes que não são cadastrados
