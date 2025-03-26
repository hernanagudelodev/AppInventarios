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
