from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Ordem)
admin.site.register(OrdemItem)
admin.site.register(EnderecoEntrega)
