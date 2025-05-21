from django.contrib import admin
from .models import *

@admin.register(TipoPropiedad)
class TipoPropiedadAdmin(admin.ModelAdmin):
    pass

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    pass

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    pass

@admin.register(PropiedadCliente)
class PropiedadClienteAdmin(admin.ModelAdmin):
    pass

@admin.register(FormularioCaptacion)
class FormularioCaptacionAdmin(admin.ModelAdmin):
    pass

@admin.register(DetallePropiedad)
class DetallePropiedadAdmin(admin.ModelAdmin):
    list_display = ('nombre','tipo_campo','tipo_detalle')

@admin.register(AltDetallesExteriores)
class AltDetallesExterioresAdmin(admin.ModelAdmin):
    pass

@admin.register(AltDetallesInteriores)
class AltDetallesInterioresAdmin(admin.ModelAdmin):
    pass

@admin.register(AltDetallesGenerales)
class AltDetallesGeneralesAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemBase)
class ItemBaseAdmin(admin.ModelAdmin):
    list_display = ('nombre_item', 'tipo_ambiente')
    list_filter = ('tipo_ambiente',)
    search_fields = ('nombre_item',)


class ItemEntregaInline(admin.TabularInline):
    model = ItemEntrega
    extra = 0


class AmbienteEntregaInline(admin.TabularInline):
    model = AmbienteEntrega
    extra = 0


@admin.register(FormularioEntrega)
class FormularioEntregaAdmin(admin.ModelAdmin):
    list_display = ('propiedad_cliente', 'fecha_entrega', 'creado')
    list_filter = ('propiedad_cliente__propiedad',)
    inlines = [AmbienteEntregaInline]


@admin.register(AmbienteEntrega)
class AmbienteEntregaAdmin(admin.ModelAdmin):
    list_display = ('formulario_entrega', 'tipo_ambiente', 'numero_ambiente')
    inlines = [ItemEntregaInline]