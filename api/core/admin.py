from django.contrib import admin
from .models import (
    Produto,
    Cliente,
    Vendedor,
    Movimento,
    Venda,
    ItemVenda,
    Financeiro
)


# =========================
# PRODUTO
# =========================
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'referencia', 'descricao', 'preco', 'saldo', 'ativo')
    search_fields = ('referencia', 'descricao')
    list_filter = ('ativo',)
    readonly_fields = ('saldo',)


# =========================
# CLIENTE
# =========================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)


# =========================
# VENDEDOR
# =========================
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)


# =========================
# MOVIMENTO (ESTOQUE)
# =========================
@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'produto',
        'tipo_mov',
        'quantidade_mov',
        'valor_mov',
    )
    list_filter = ('tipo_mov',)
    autocomplete_fields = ('produto',)


# =========================
# ITEM VENDA (INLINE)
# =========================
class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1


# =========================
# VENDA
# =========================
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'cliente',
        'vendedor',
        'valor_total',
    )
    list_filter = ('status',)
    autocomplete_fields = ('cliente', 'vendedor')
    readonly_fields = ('valor_total',)
    inlines = [ItemVendaInline]


# =========================
# FINANCEIRO
# =========================
@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo',
        'pago',
        'cliente',
        'vendedor',
        'valor_parcela',
        'saldo_parcela'
    )
    list_filter = ('tipo', 'pago')
    autocomplete_fields = ('cliente', 'vendedor')
