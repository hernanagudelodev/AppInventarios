from django.urls import path
from . import views

app_name = 'inventarioAPP'

urlpatterns = [
    path('', views.home,name='home'),
    path('clientes/lista/', views.ListaClientes.as_view(),name='lista_clientes'),
    path('clientes/crear/', views.CrearCliente.as_view(),name='crear_cliente'),
    path('clientes/actualizar/<int:pk>/', views.ActualizarCliente.as_view(), name='actualizar_cliente'),
    path('clientes/detalle/<int:pk>/', views.DetalleCliente.as_view(), name='detalle_cliente'),
    path('propiedades/lista/', views.ListaPropiedades.as_view(),name='lista_propiedades'),
    path('clientes/eliminar/<int:pk>/', views.EliminarCliente.as_view(), name='eliminar_cliente'),
    path('propiedades/crear/', views.CrearPropiedad.as_view(),name='crear_propiedad'),
    path('propiedades/actualizar/<int:pk>/', views.ActualizarPropiedad.as_view(), name='actualizar_propiedad'),
    path('propiedades/detalle/<int:id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('propiedades/captacion/<int:id>/', views.Altnuevo_formulario_captacion, name='nueva_captacion'),
    path('asistenteAI/estimador/', views.estimador_view ,name='estimador_m2'),
    path('asistenteAI/api/get_regiones/', views.get_regiones, name='get_regiones'),
    path('asistenteAI/api/get_ciudades/', views.get_ciudades, name='get_ciudades'),
]