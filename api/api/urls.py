"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('produtos/',views.ProdutoView.as_view(),name='produtos'),
    path('produtos/cadastro/',views.CadastroProduto.as_view(),name='cadastroproduto'),
    path('produtos/<int:id>',views.ProdutoViewUnico.as_view(),name='editarproduto'),
    path('produtos/<int:id>/ajuste',views.AjustarProduto.as_view(),name='ajustarestoque'),
    path('movimentos/',views.VizualizarMovimento.as_view(),name='movimentos'),
    path('movimentos/<int:produto_id>',views.VizualizarMovimentoDoItem.as_view(),name='movimentoitem'),
    path('clientes/',views.ClienteView.as_view(),name='clientes'),
    path('clientes/<int:id>',views.ClienteEdit.as_view(),name='editarcliente'),
    path('clientes/cadastro/',views.CadastroCliente.as_view(),name='cadastrocliente'),
    path('vendedores/',views.VendedorView.as_view(),name='vendedores'),
    path('vendedores/<int:id>',views.VendedorEdit.as_view(),name='editarvendedor'),
    path('vendedores/cadastro/',views.CadastroVendedor.as_view(),name='cadastrovendedor'),
    path('vendas/',views.VendaView.as_view(),name='vendas'),
    path('vendas/gerarvenda',views.GerarVenda.as_view(),name='gerarvenda')
]
