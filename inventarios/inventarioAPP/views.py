from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.forms import formset_factory
from .estimador import asistente_estimador_dinamico
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from .wasi_api import *
import os
from django.core.files.base import ContentFile
import base64
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
os.environ['WEASYPRINT_DLL_DIRECTORIES'] = r'C:\Program Files\GTK3-Runtime Win64\bin'
from weasyprint import HTML
from io import BytesIO
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from collections import defaultdict


def _get_secciones_valores(captacion):
    """
    Retorna una lista de tuplas (seccion, [(nombre_campo, valor), ...])
    para el formulario de captación dado.
    """
    secciones_dict = defaultdict(list)
    for valor in captacion.valores.select_related('campo__seccion').all():
        seccion = valor.campo.seccion
        # Formatea el valor según el tipo de campo
        if valor.campo.tipo == 'texto':
            val = valor.valor_texto
        elif valor.campo.tipo == 'numero':
            val = valor.valor_numero
        elif valor.campo.tipo == 'booleano':
            val = "Sí" if valor.valor_booleano else "No"
        else:
            val = ""
        secciones_dict[seccion].append((valor.campo.nombre, val))
    # Ordena las secciones por su campo 'orden'
    secciones = sorted(secciones_dict.keys(), key=lambda s: s.orden)
    return [(seccion, secciones_dict[seccion]) for seccion in secciones]

@login_required
def home(request):
    return render(
        request,
        'inventarioapp/home.html',
        {'section':'home'}
    )

''' 
A partir de este momento hacemos las vistas para manejar clientes. Estas se hacen
heredando de generic views.
'''

class CrearCliente(LoginRequiredMixin,CreateView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('inventarioapp:lista_clientes')
    template_name = "inventarioapp/clientes/form_cliente.html"

class ListaClientes(LoginRequiredMixin,ListView):
    model = Cliente
    fields = '__all__'
    context_object_name = 'clientes'
    template_name = "inventarioapp/clientes/lista_clientes.html"

class ActualizarCliente(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('inventarioapp:lista_clientes')
    template_name = "inventarioapp/clientes/form_cliente.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actualizar'] = True
        return context
    
class EliminarCliente(LoginRequiredMixin, DeleteView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('inventarioapp:lista_clientes')
    template_name = "inventarioapp/clientes/borrar_cliente.html"

class DetalleCliente(LoginRequiredMixin,DetailView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('inventarioapp:lista_clientes')
    template_name = "inventarioapp/clientes/detalle_cliente.html"
    

'''
A partir de esta linea se crearan las vistas para CRUD de propiedades
'''

class ListaPropiedades(LoginRequiredMixin,ListView):
    model = Propiedad
    fields = '__all__'
    context_object_name = 'propiedades'
    template_name = "inventarioapp/propiedades/lista_propiedades.html"

def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            propiedad = form.save()
            messages.success(request, "Propiedad creada exitosamente.")
            return redirect('inventarioapp:detalle_propiedad', id=propiedad.id)
    else:
        form = PropiedadForm()
    return render(request, 'inventarioapp/propiedades/form_propiedad.html', {
        'form': form
    })


def actualizar_propiedad(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad actualizada exitosamente.")
            return redirect('inventarioapp:detalle_propiedad', id=propiedad.id)
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'inventarioapp/propiedades/form_propiedad.html', {
        'form': form,
        'actualizar': True,
        'propiedad': propiedad,
    })

def agregar_relacion_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if request.method == 'POST':
        form = AgregarPropiedadClienteForm(request.POST, propiedad=propiedad)
        if form.is_valid():
            relacion = form.save(commit=False)
            relacion.propiedad = propiedad
            relacion.save()
            messages.success(request, "Relación agregada correctamente.")
            return redirect('inventarioapp:detalle_propiedad', id=propiedad.id)
    else:
        form = AgregarPropiedadClienteForm(propiedad=propiedad)
    return render(request, 'inventarioapp/propiedades/agregar_relacion.html', {
        'form': form,
        'propiedad': propiedad,
    })

def eliminar_relacion_propiedad(request, relacion_id):
    relacion = get_object_or_404(PropiedadCliente, id=relacion_id)
    propiedad_id = relacion.propiedad.id
    if request.method == 'POST':
        relacion.delete()
        messages.success(request, "Relación eliminada correctamente.")
    return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)

@login_required
def detalle_propiedad(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    # Relacionados a la propiedad
    relaciones = propiedad.propiedadcliente_set.all()
    captaciones = FormularioCaptacion.objects.filter(propiedad_cliente__in=relaciones)
    entregas = FormularioEntrega.objects.filter(propiedad_cliente__in=relaciones)
    puede_entregar = FormularioCaptacion.objects.filter(
        propiedad_cliente__propiedad=propiedad,
        is_firmado=True
    ).exists()
    return render(
        request,
        'inventarioapp/propiedades/detalle_propiedad_completo.html',
        {
            'propiedad': propiedad,
            'captaciones': captaciones,
            'entregas': entregas,
            'puede_entregar': puede_entregar,
        }
    )

'''
A partir de esta linea se crearan las vistas para CRUD de DetallePropiedad
No lo voy a hacer directamente sino como una tabla relacionada a TipoPropiedad
'''


# '''
# Acá inician las funciones y metodos para manejar la creación y modificación de formularios
# de captación'''

# # Esta función se utiliza para crear un formulario de captación en blanco
# '''
# Creo que a esto hay que hacerle una revisión desde el proceso.
# Como está definido, solo se puede crear un formulario de captación por propiedad.
# Es posible que esté bien, pero en el caso que la propiedad se capte para venta o renta
# varias veces, de diferentes dueños... se tendría que crear la propiedad nuevamente.

# Es posible que lo mejor que se pueda hacer es no permitir que se borre la relación de tipo
# propietario de una propiedad, el problema es que se pueden agregar varios propietarios a una
# propiedad.
# '''
# def formulario_captacion_propiedad(propiedad: Propiedad):
#     #Primero se valida si ya existe el formulario de captación
#     try:
#         formulario_captacion = FormularioCaptacion.objects.get(propiedad=propiedad)
#     except FormularioCaptacion.DoesNotExist:
#         # sino existe se crea nuevo
#         formulario_captacion = FormularioCaptacion(propiedad=propiedad,fecha=datetime.now())
#         formulario_captacion.save()
#     #Se consulta el tipo de propiedad al que corresponde la propiedad.
#     tipo_propiedad = formulario_captacion.propiedad.tipo_propiedad 
#     # Se filtran todos los detalles de propiedad según el tipo de propiedad
#     detalle_propiedad = DetallePropiedad.objects.all().filter(clase_propiedad=tipo_propiedad)
#     try:
#         # Se valida si existen ya los detalles de captación
#         detalle_captacion = DetalleCaptacion.objects.get(formulario_captacion=formulario_captacion)
#     except DetalleCaptacion.DoesNotExist:
#         # Sino, para cada detalle, en los detalles de propiedad
#         for detalle in detalle_propiedad:
#             # Se crea un nuevo detalle de captación
#             detalle_captacion = DetalleCaptacion(detalle_propiedad=detalle,formulario_captacion=formulario_captacion)
#             detalle_captacion.save()
#     except DetalleCaptacion.MultipleObjectsReturned:
#         pass
#     return formulario_captacion

# # Este metodo permite construir un formset que tiene todos los campos de formulario de captación
# # cada uno como un form
# '''
# PENDIENTE: Aun esta pendiente hacer la validación del tipo de dato que se puede escribir en cada detalle de captación
# según la información almacenada en la base de datos.
# '''
# def contruir_formulario_captacion(formulario_captacion):
#     # Lo primero es definir el formset vacio, que recibe el parametro del form detalle de captación
#     detalle_captacion_formset = formset_factory(detalleCaptacionForm)
#     # Se consulta de la base de datos el queryset de todos los detalles de captación (formularios) que deben salir en el formset
#     detalles_captacion = DetalleCaptacion.objects.all().filter(formulario_captacion=formulario_captacion)
#     # Se define la cantidad de formularios que van a salir en el formset
#     formularios_totales = detalles_captacion.count()
#     # Se define el diccionario inicial con dos parametros, el total de formularios y los formularios iniciales.
#     data = {
#         "form-TOTAL_FORMS": formularios_totales,
#         "form-INITIAL_FORMS": "0",
#     }
#     #Esta variable me sirve para contar... sin embargo esto se debe poder hacer mejor, cuando encuentre la forma de mejorar esto, lo cambio.
#     i = 0
#     # este for va a recorrer cada uno de los registros del queryset, para agregarlos al diccionario data del formset.
#     for detalle_captacion in detalles_captacion:
#          #Se define el indice a agregar en el data, este es un nombre estandar para los forms de un formset
#          index = "form-" + str(i) + "-detalle"
#          #Se define el valor a mostrar en el campo del formulario
#          value = detalle_captacion.detalle # esto es temporal, solo para probar, el value es "detalle"
#          # se agrega el registro al formulario
#          data[index] = value
#          i = i + 1

#     # se pasa el diccionario de configuración al formset
#     formset = detalle_captacion_formset(data)
    
#     # Se reinicia esta variable, nuevamente esto se debe poder hacer de forma diferente
#     i = 0
#     # Este for recorre el formset para cambiar el label de cada form y ponerle el nombre del detalle propiedad 
#     # correspondiente al formulario detalle captación
#     for form in formset:
#         # Se carga el valor que se va a dar al label
#         value = detalles_captacion[i].detalle_propiedad
#         # nombre_campo = "id_form-" + str(i) + "-detalle"
#         # Se asigna el valor al label del correspondiente formulario
#         form.fields['detalle'].label = value.nombre
#         print(form)
#         i = i + 1
#     #Se retorna el formset que se construyó
#     return formset


# # Este metodo es llamado para crear un nuevo formulario, desde la URL
# # Recibe el request y un parametro ID que es el identificador de la propiedad
# '''
# PENDIENTE: Aún está pendiente guardar los datos que se ingresan en el formulario al darle "guardar"
# '''
# @login_required
# def nuevo_formulario_captacion(request,id):
#     # Obtenemos el objeto propiedad al cual se le creaará el formulario de captación
#     propiedad = Propiedad.objects.get(id=id) 
#     # Se llama la función que crea, cuando no existe, o carga el formulario de captación de la propiedad
#     formulario_captacion = formulario_captacion_propiedad(propiedad) 
#     # Se cargar los detalles de captación del formulario, estos se usarán para personalizar el formset de detalles de captación
#     detalles_captacion = DetalleCaptacion.objects.all().filter(formulario_captacion=formulario_captacion)
#     # Se instancia el formset de detalles de captación. A esto se le debe hacer más configuración.
#     detalle_captacion_formset = contruir_formulario_captacion(formulario_captacion)
#     if request.method == 'POST':
#         captacion_form = CaptacionForm(instance=formulario_captacion,
#                                        data=request.POST)
#         if captacion_form.is_valid():
#             captacion_form.save()
#             messages.success(request, 'Profile updated successfully')
#         else:
#             messages.error(request, 'Error updating your profile')
#     else:
#         captacion_form = CaptacionForm(instance=formulario_captacion)
#         # detalles_captacion_form = detalleCaptacionForm(qs=detalles_captacion)
#     return render(
#         request,
#         'inventarioapp/captacion/formulario_captacion.html',
#         {'formulario_captacion':formulario_captacion,
#          'propiedad':propiedad,
#          'form':captacion_form,
#          'form2':detalle_captacion_formset,
#          'detalles_captacion':detalles_captacion}
#     )

#     '''
#     <form method="post" enctype="multipart/form-data">
#         {{ form.as_p }}
#         {{ form2.as_p }}
#         {% csrf_token %}
#         <p><input type="submit" value="Guardar Formulario"></p>
#     </form>



#     <form action="" method="post">
#         {% csrf_token %}
#         {{ form.as_p }}
#         <input type="submit" value="Actualizar Cliente">
#     </form>
#     '''


# # '''
# # CAMINO TEMPORAL - SE BORRA PARA DAR PASO A UN NUEVO CAMINO DE FORMULARIO DE CAPTACIÓN
# # A partir de acá, y para poder terminar el MVP, voy a cambiar de estrategía y voy a crear formularios ModelForm a base de datos
# # que no sean configurables. Esto para tener un entregable rápido.
# # '''

# # #Este método crea, sino existe, un formulario de captación para una propiedad determinada. Este es en blanco.
# # #La idea es evitar multiples formularios, y cargar el formulario para la función que se encarga de manejar el formulario de captación
# # #tambien se crean los detalles del formulario de captación
# # def Altformulario_captacion_propiedad(propiedad: Propiedad):
#     #Primero se valida si ya existe el formulario de captación
#     try:
#         formulario_captacion = FormularioCaptacion.objects.get(propiedad=propiedad)
#     except FormularioCaptacion.DoesNotExist:
#         # sino existe el formulario de captación se crea uno nuevo
#         formulario_captacion = FormularioCaptacion(propiedad=propiedad,fecha=datetime.now())
#         formulario_captacion.save()
#         # con el formulario de captación, se crean los detalles del formulario
#         detalles_exteriores = AltDetallesExteriores(formulario_captacion=formulario_captacion)
#         detalles_interiores = AltDetallesInteriores(formulario_captacion=formulario_captacion)
#         detalles_generales = AltDetallesGenerales(formulario_captacion=formulario_captacion)
#         detalles_exteriores.save()
#         detalles_interiores.save()
#         detalles_generales.save()
#     return formulario_captacion


# '''
# Función que maneja el formulario de captación, recibe el id de la propiedad
# '''
# @login_required
# def Altnuevo_formulario_captacion(request,id):
#     # Obtenemos el objeto propiedad al cual se le creaará el formulario de captación
#     propiedad = Propiedad.objects.get(id=id) 
#     # Se llama la función que crea, cuando no existe, o carga el formulario de captación de la propiedad
#     formulario_captacion = Altformulario_captacion_propiedad(propiedad)
#     # se cargan los detalles generales, interiores y exteriores del formulario de captación
#     det_generales_captacion = AltDetallesGenerales.objects.get(formulario_captacion=formulario_captacion)
#     det_interiores_captación = AltDetallesInteriores.objects.get(formulario_captacion=formulario_captacion)
#     det_exteriores_captacion = AltDetallesExteriores.objects.get(formulario_captacion=formulario_captacion)
#     # Si se recibe el metodo POST, se cargan los form del formulario de captación y de los detalles, con la información del data del post.
#     if request.method == 'POST':
#         captacion_form = CaptacionForm(instance=formulario_captacion,
#                                        data=request.POST)
#         det_generales_captacion_form = detallesGeneralesCaptacionForm(instance=det_generales_captacion,
#                                        data=request.POST)
#         det_interiores_captacion_form = detallesInterioresCaptacionForm(instance=det_interiores_captación,
#                                        data=request.POST)
#         det_exteriores_captacion_form = detallesExterioresCaptacionForm(instance=det_exteriores_captacion,
#                                        data=request.POST)
#         # Se valida si los formularios son validos, y si es así, se guardan.
#         if captacion_form.is_valid():
#             captacion_form.save()
#             messages.success(request, 'Información básica del proceso de captación guardada')
#         else:
#             messages.error(request, 'Error guardando la información básica del proceso de captación')
#         if det_generales_captacion_form.is_valid():
#             det_generales_captacion_form.save()
#             messages.success(request, 'Detalles generales del formulario de captación guardados')
#         else:
#             messages.error(request, 'Error guardando los detalles generales del formulario de captación')
#         if det_interiores_captacion_form.is_valid():
#             det_interiores_captacion_form.save()
#             messages.success(request, 'Detalles interiores del formulario de captación guardados')
#         else:
#             messages.error(request, 'Error guardando los detalles interiores del formulario de captación')
#         if det_exteriores_captacion_form.is_valid():
#             det_exteriores_captacion_form.save()
#             messages.success(request, 'Detalles generales del formulario de captación guardados')
#         else:
#             messages.error(request, 'Error guardando los detalles generales del formulario de captación')
#     else: # Si no es el metodo POST, se cargan los form con la información de la base de datos
#         captacion_form = CaptacionForm(instance=formulario_captacion)
#         det_generales_captacion_form = detallesGeneralesCaptacionForm(instance=det_generales_captacion)
#         det_interiores_captacion_form = detallesInterioresCaptacionForm(instance=det_interiores_captación)
#         det_exteriores_captacion_form = detallesExterioresCaptacionForm(instance=det_exteriores_captacion)
#     #Se genera el render donde se define el template, y se envian los forms
#     return render(
#         request,
#         'inventarioapp/captacion/formulario_captacion.html',
#         {'formulario_captacion':formulario_captacion,
#          'propiedad':propiedad,
#          'form':captacion_form,
#          'form2':det_generales_captacion_form,
#          'form3':det_interiores_captacion_form,
#          'form4':det_exteriores_captacion_form
#          }
#     )

'''
Vista para estimar precio del metro cuadrado de una propiedad según varios filtros
'''
def estimador_view(request):
    resultado = None
    if request.method == 'POST':
        form = EstimadorForm(request.POST)
        if form.is_valid():
            area = form.cleaned_data['area_objetivo']
            city = form.cleaned_data['id_city']
            zone = form.cleaned_data.get('id_zone')
            location = form.cleaned_data.get('id_location')

            resultado = asistente_estimador_dinamico(
                area_objetivo=area,
                id_company='TU_ID_COMPANY',
                wasi_token='TU_TOKEN',
                id_city=city,
                id_location=location,
                id_zone=zone
            )
        else:
            # Si el form no es válido, lo volvemos a renderizar con los datos que tiene
            form = EstimadorForm(request.POST)
    else:
        form = EstimadorForm()
    return render(request,
                   'inventarioapp/asistenteAI/estimador_m2.html',
                   {'form': form, 'resultado': resultado})


def get_regiones(request):
    if request.method == "GET":
        id_country = request.GET.get("id_country")
        regiones = obtener_regiones(id_country)
        return JsonResponse({"regiones": regiones})

def get_ciudades(request):
    if request.method == "GET":
        id_region = request.GET.get("id_region")
        ciudades = obtener_ciudades(id_region)
        return JsonResponse({"ciudades": ciudades})

def get_localidades(request):
    if request.method == "GET":
        id_city = request.GET.get("id_city")
        localidades = obtener_localidades(id_city)
        return JsonResponse({"localidades": localidades})

def get_zonas(request):
    if request.method == "GET":
        id_city = request.GET.get("id_city")
        zonas = obtener_zonas(id_city)
        return JsonResponse({"zonas": zonas})

'''
FORMULARIO DE ENTREGA
A partir de esta linea se hacen las vistas para la creación de formularios de entrega
'''

'''
La primera vista crea la relación entre cliente y propiedad.
'''
def crear_formulario_entrega(request):
    if request.method == 'POST':
        form = SeleccionarPropiedadClienteForm(request.POST)
        if form.is_valid():
            propiedad = form.cleaned_data['propiedad']
            # Verifica si hay captación firmada para esta propiedad
            captacion_firmada = FormularioCaptacion.objects.filter(
                propiedad_cliente__propiedad=propiedad,
                is_firmado=True
            ).exists()
            if not captacion_firmada:
                messages.error(
                    request,
                    "No se puede crear un formulario de entrega: no existe una captación firmada para esta propiedad."
                )
                return redirect('inventarioapp:detalle_propiedad', id=propiedad.id)
            
            # Si pasa la validación, continúa el flujo
            prop_cliente = form.save()
            entrega = FormularioEntrega.objects.create(propiedad_cliente=prop_cliente)
            messages.success(request, "Formulario de entrega creado exitosamente.")
            return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)
    else:
        form = SeleccionarPropiedadClienteForm()
    return render(request, 'inventarioapp/entrega/crear_formulario_entrega.html', {'form': form})

'''
Esta vista permite agregar ambiente al formulario de entrega.
'''

def agregar_ambiente(request, entrega_id):
    entrega = get_object_or_404(FormularioEntrega, id=entrega_id)

    if entrega.is_firmado:
        messages.error(request, "Este formulario ya fue firmado y no puede modificarse.")
        return redirect('inventarioapp:ver_pdf_formulario_entrega', entrega_id=entrega.id)

    if request.method == 'POST':
        form = AmbienteEntregaForm(request.POST)
        if form.is_valid():
            ambiente = form.save(commit=False)
            ambiente.formulario_entrega = entrega
            ambiente.save()
            return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)
    else:
        form = AmbienteEntregaForm()

    ambientes_existentes = entrega.ambientes.all()
    return render(request, 'inventarioapp/entrega/agregar_ambiente.html', {
        'form': form,
        'entrega': entrega,
        'ambientes': ambientes_existentes
    })


'''
Esta vista permite modificar los items de un ambiente de un formulario de entrega
'''
def editar_items_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(AmbienteEntrega, id=ambiente_id)
    formset = ItemEntregaFormSet(queryset=ambiente.items.all())

    if request.method == 'POST':
        formset = ItemEntregaFormSet(request.POST, queryset=ambiente.items.all())
        if formset.is_valid():
            formset.save()
            return redirect('inventarioapp:agregar_ambiente', entrega_id=ambiente.formulario_entrega.id)
        else:
            print(formset.errors)

    return render(request, 'inventarioapp/entrega/editar_items_ambiente.html', {
        'ambiente': ambiente,
        'formset': formset,
    })

'''
Esta vista permite ver el resumen de un formulario de entrega y firmarlo
'''
def resumen_formulario_entrega(request, entrega_id):
    entrega = get_object_or_404(FormularioEntrega, id=entrega_id)

    if request.method == 'POST':
        firma_data = request.POST.get('firma_base64')
        try:
            if firma_data and not entrega.firma_cliente:
                format, imgstr = firma_data.split(';base64,') 
                entrega.firma_cliente.save(f'firma_{entrega.id}.png', ContentFile(base64.b64decode(imgstr)), save=True)
                entrega.is_firmado = True
                entrega.fecha_firma = timezone.now()
                entrega.save()
                firma_dir = os.path.join(settings.MEDIA_ROOT, 'firmas')
                os.makedirs(firma_dir, exist_ok=True)

                file_path = os.path.join(firma_dir, f'firma_{entrega_id}.png')
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(firma_data.split(',')[1]))
                # Por si querés mostrar la URL luego:
                firma_url = settings.MEDIA_URL + f'firmas/firma_{entrega_id}.png'
                messages.success(request, "Firma guardada exitosamente.")
            else:
                messages.error(request, "No se recibió firma válida o ya estaba firmada.")
        except Exception as e:
            messages.error(request, f"Error al guardar la firma: {e}")
        return redirect('inventarioapp:resumen_formulario_entrega', entrega_id=entrega_id)
    
    ambientes = entrega.ambientes.prefetch_related('items').all()
    return render(request, 'inventarioapp/entrega/resumen_formulario.html', {
        'entrega': entrega,
        'ambientes': ambientes
    })

'''
Función para envio de formulario en pdf por correo electrónico
'''
def enviar_formulario_pdf(request, entrega_id):
    entrega = get_object_or_404(FormularioEntrega, id=entrega_id)
    ambientes = entrega.ambientes.prefetch_related('items').all()

    html_string = render_to_string('inventarioapp/entrega/resumen_pdf.html', {
        'entrega': entrega,
        'ambientes': ambientes
    })

    pdf_file = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target=pdf_file)

    email = EmailMessage(
        'Formulario de Entrega',
        'Adjunto encontrarás el PDF del inventario firmado.',
        'comercial2.stanza@gmail.com',
        [entrega.propiedad_cliente.cliente.email],
    )
    email.attach(f'formulario_entrega_{entrega_id}.pdf', pdf_file.getvalue(), 'application/pdf')
    email.send()

    propiedad = entrega.propiedad

    messages.success(request, "Formulario enviado por correo.")
    return redirect('inventarioapp:formularios_entrega_propiedad', propiedad_id=propiedad.id)


'''
Función para descargar el pdf una vez firmado.
'''
def ver_pdf_formulario_entrega(request, entrega_id):
    entrega = get_object_or_404(FormularioEntrega, id=entrega_id)
    ambientes = entrega.ambientes.prefetch_related('items').all()

    html_string = render_to_string('inventarioapp/entrega/resumen_pdf.html', {
        'entrega': entrega,
        'ambientes': ambientes
    })

    pdf_file = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target=pdf_file)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=formulario_entrega_{entrega_id}.pdf'
    return response


'''
Función que carga el formulario de entregas de una propiedad
'''
def formularios_entrega_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    entregas = FormularioEntrega.objects.filter(propiedad_cliente__propiedad=propiedad)
    return render(request, 'inventarioapp/entrega/lista_entregas.html', {
        'propiedad': propiedad,
        'entregas': entregas
    })

'''
función para editar ambiente, el objetivo es editar el nombre del ambiente, esto lo permite hacer en la pantalla de agregar ambiente
'''
def editar_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(AmbienteEntrega, id=ambiente_id)
    entrega = ambiente.formulario_entrega

    if entrega.is_firmado:
        messages.error(request, "No se puede editar un ambiente en un formulario firmado.")
        return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        if nuevo_nombre:
            ambiente.nombre_personalizado = nuevo_nombre
            ambiente.save()
            messages.success(request, "Ambiente actualizado exitosamente.")
            return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)
        else:
            messages.error(request, "El nombre no puede estar vacío.")

    return render(request, 'inventarioapp/entrega/editar_ambiente.html', {'ambiente': ambiente})

'''
Función para eliminar ambiente, esta será llamada desde la vista de agregar ambiente
'''
def eliminar_ambiente(request, ambiente_id):
    ambiente = get_object_or_404(AmbienteEntrega, id=ambiente_id)
    entrega = ambiente.formulario_entrega

    if entrega.is_firmado:
        messages.error(request, "No se puede eliminar un ambiente en un formulario firmado.")
        return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)

    if request.method == 'POST':
        ambiente.delete()
        messages.success(request, "Ambiente eliminado exitosamente.")
        return redirect('inventarioapp:agregar_ambiente', entrega_id=entrega.id)

    return render(request, 'inventarioapp/entrega/confirmar_eliminar_ambiente.html', {'ambiente': ambiente})

'''
Función de eliminar items de ambientes
'''
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemEntrega, id=item_id)
    ambiente = item.ambiente_entrega
    entrega = ambiente.formulario_entrega

    if entrega.is_firmado:
        messages.error(request, "No se puede eliminar un ítem de un formulario firmado.")
        return redirect('inventarioapp:editar_items_ambiente', ambiente_id=ambiente.id)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Ítem eliminado exitosamente.")
        return redirect('inventarioapp:editar_items_ambiente', ambiente_id=ambiente.id)

    return render(request, 'inventarioapp/entrega/confirmar_eliminar_item.html', {'item': item})

'''
Función para confirmar envío por correo electrónico del formulario de entrega
'''
def confirmar_envio_correo(request, entrega_id):
    entrega = get_object_or_404(FormularioEntrega, id=entrega_id)
    cliente = entrega.propiedad_cliente.cliente

    if not entrega.is_firmado:
        messages.error(request, "El formulario debe estar firmado antes de enviarlo.")
        return redirect('inventarioapp:resumen_formulario_entrega', entrega_id=entrega.id)

    if request.method == 'POST':
        correo_ingresado = request.POST.get('correo')
        try:
            validate_email(correo_ingresado)
            cliente.email = correo_ingresado
            cliente.save()
            return redirect('inventarioapp:enviar_formulario_pdf', entrega_id=entrega.id)
        except ValidationError:
            messages.error(request, "Por favor, ingresa un correo electrónico válido.")

    return render(request, 'inventarioapp/entrega/confirmar_envio_correo.html', {
        'entrega': entrega,
        'cliente_email': cliente.email or ''
    })


'''
NUEVAS VISTAS MODELO DE CAPTACION
A partir de esta linea se implementa un nuevo modelo de inventario de captación
'''

'''
Función para vista que obtiene los clientes relacionados con una propiedad
'''
def seleccionar_cliente_para_captacion(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    relaciones = PropiedadCliente.objects.filter(propiedad=propiedad)
    if request.method == 'POST':
        relacion_id = request.POST.get('relacion_id')
        return redirect('inventarioapp:formulario_captacion', relacion_id=relacion_id)
    return render(request, 'inventarioapp/captacion/seleccionar_cliente_captacion.html', {
        'propiedad': propiedad,
        'relaciones': relaciones,
    })

'''
Función para crear el formulario de captación dínamico según lo guardado en CampoCaptacion y SeccionCaptacion
'''
def formulario_captacion_dinamico(request, relacion_id):
    relacion = get_object_or_404(PropiedadCliente, id=relacion_id)
    if request.method == 'POST':
        form = FormularioCaptacionDinamico(request.POST)
        if form.is_valid():
            # 1. Crear el formulario de captación
            captacion = FormularioCaptacion.objects.create(
                propiedad_cliente=relacion,
                creado=timezone.now()
            )
            # 2. Guardar cada campo
            for key, value in form.cleaned_data.items():
                campo_id = int(key.replace('campo_', ''))
                campo = CampoCaptacion.objects.get(id=campo_id)
                if campo.tipo == 'texto':
                    ValorCampoCaptacion.objects.create(
                        formulario=captacion,
                        campo=campo,
                        valor_texto=value
                    )
                elif campo.tipo == 'numero':
                    ValorCampoCaptacion.objects.create(
                        formulario=captacion,
                        campo=campo,
                        valor_numero=value
                    )
                elif campo.tipo == 'booleano':
                    ValorCampoCaptacion.objects.create(
                        formulario=captacion,
                        campo=campo,
                        valor_booleano=value
                    )
            # 3. Redirigir a una vista de éxito, detalle, o lo que prefieras
            propiedad_id = captacion.propiedad_cliente.propiedad.id
            return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)
    else:
        form = FormularioCaptacionDinamico()
    secciones_fields = []
    for seccion in form.secciones:
        campos = [form[field_name] for field_name in seccion['campos']]
        secciones_fields.append({'nombre': seccion['nombre'], 'campos': campos})

    return render(request, 'inventarioapp/captacion/formulario_captacion_dinamico.html', {
        'form': form,
        'relacion': relacion,
        'secciones_fields': secciones_fields,
    })

'''
Función para vista de resumen de formulario de captación
'''
def resumen_formulario_captacion(request, captacion_id):
    captacion = get_object_or_404(FormularioCaptacion, id=captacion_id)

    if request.method == 'POST':
        firma_data = request.POST.get('firma_base64')
        try:
            if firma_data and not captacion.firma_cliente:
                format, imgstr = firma_data.split(';base64,')
                captacion.firma_cliente.save(f'firma_captacion_{captacion.id}.png', ContentFile(base64.b64decode(imgstr)), save=True)
                captacion.is_firmado = True
                captacion.fecha_firma = timezone.now()
                captacion.save()
                firma_dir = os.path.join(settings.MEDIA_ROOT, 'firmas_captacion')
                os.makedirs(firma_dir, exist_ok=True)
                file_path = os.path.join(firma_dir, f'firma_captacion_{captacion_id}.png')
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(imgstr))
                firma_url = settings.MEDIA_URL + f'firmas_captacion/firma_captacion_{captacion_id}.png'
                messages.success(request, "Firma guardada exitosamente.")
            else:
                messages.error(request, "No se recibió firma válida o ya estaba firmada.")
        except Exception as e:
            messages.error(request, f"Error al guardar la firma: {e}")
        return redirect('inventarioapp:resumen_formulario_captacion', captacion_id=captacion_id)

    secciones_valores = _get_secciones_valores(captacion)

    return render(request, 'inventarioapp/captacion/resumen_formulario_captacion.html', {
        'captacion': captacion,
        'secciones_valores': secciones_valores,
    })

'''
Función para envio de formulario de captación por correo electrónico, en pdf
'''
def enviar_formulario_captacion(request, captacion_id):
    captacion = get_object_or_404(FormularioCaptacion, id=captacion_id)
    cliente = captacion.cliente
    cliente_email = cliente.email

    if request.method == 'POST':
        correo = request.POST.get('correo')
        # Render HTML del PDF
        html_string = render_to_string('inventarioapp/captacion/resumen_pdf_captacion.html', {
            'captacion': captacion,
            # Pasa también las secciones/campos si los usas en el PDF:
            'secciones_valores': _get_secciones_valores(captacion),
        })
        pdf_file = BytesIO()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target=pdf_file)

        email = EmailMessage(
            'Formulario de Captación Firmado',
            'Adjunto encontrarás el PDF del formulario de captación firmado.',
            'comercial2.stanza@gmail.com',  # Cambia si quieres
            [correo],
        )
        email.attach(f'formulario_captacion_{captacion.id}.pdf', pdf_file.getvalue(), 'application/pdf')
        email.send()
        messages.success(request, "Formulario enviado por correo.")
        return redirect('inventarioapp:resumen_formulario_captacion', captacion_id=captacion_id)

    return render(request, 'inventarioapp/captacion/confirmar_envio_captacion.html', {
        'captacion': captacion,
        'cliente_email': cliente_email
    })


'''
Función de eliminar captación en borrador
'''
def eliminar_captacion(request, captacion_id):
    captacion = get_object_or_404(FormularioCaptacion, id=captacion_id)
    propiedad_id = captacion.propiedad_cliente.propiedad.id

    if captacion.is_firmado:
        messages.error(request, "No se puede eliminar una captación ya firmada.")
        return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)

    if request.method == 'POST':
        captacion.delete()
        messages.success(request, "Captación eliminada correctamente.")
        return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)

    return render(request, 'inventarioapp/captacion/confirmar_eliminar_captacion.html', {
        'captacion': captacion,
        'propiedad_id': propiedad_id,
    })

'''
Función que permite editar un formulario de captación, utiliza el mismo Formulario para crear la captación
'''

def editar_captacion(request, captacion_id):
    captacion = get_object_or_404(FormularioCaptacion, id=captacion_id)
    propiedad_id = captacion.propiedad_cliente.propiedad.id
    relacion = captacion.propiedad_cliente
    if captacion.is_firmado:
        messages.error(request, "No se puede editar una captación ya firmada.")
        return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)

    # Prellenar valores actuales
    initial = {}
    for valor in captacion.valores.all():
        field_name = f'campo_{valor.campo.id}'
        if valor.campo.tipo == 'texto':
            initial[field_name] = valor.valor_texto
        elif valor.campo.tipo == 'numero':
            initial[field_name] = valor.valor_numero
        elif valor.campo.tipo == 'booleano':
            initial[field_name] = valor.valor_booleano

    if request.method == 'POST':
        form = FormularioCaptacionDinamico(request.POST, initial=initial)
        if form.is_valid():
            # Actualizar los valores
            for key, value in form.cleaned_data.items():
                campo_id = int(key.replace('campo_', ''))
                valor_obj = captacion.valores.filter(campo_id=campo_id).first()
                if valor_obj:
                    if valor_obj.campo.tipo == 'texto':
                        valor_obj.valor_texto = value
                    elif valor_obj.campo.tipo == 'numero':
                        valor_obj.valor_numero = value
                    elif valor_obj.campo.tipo == 'booleano':
                        valor_obj.valor_booleano = value
                    valor_obj.save()
            messages.success(request, "Captación editada correctamente.")
            return redirect('inventarioapp:detalle_propiedad', id=propiedad_id)
    else:
        form = FormularioCaptacionDinamico(initial=initial)

    # --- Construcción de secciones_fields para el template ---
    secciones_fields = []
    for seccion in form.secciones:
        campos = [form[field_name] for field_name in seccion['campos']]
        secciones_fields.append({'nombre': seccion['nombre'], 'campos': campos})

    return render(request, 'inventarioapp/captacion/formulario_captacion_dinamico.html', {
        'form': form,
        'captacion': captacion,
        'secciones_fields': secciones_fields,
        'modo_edicion': True,
        'relacion': relacion,
    })


