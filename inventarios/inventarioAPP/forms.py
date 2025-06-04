from django import forms
from django.forms import modelformset_factory
from .models import *
from django.forms.formsets import Form, BaseFormSet, formset_factory, ValidationError
from .wasi_api import obtener_paises, obtener_regiones, obtener_ciudades, obtener_localidades, obtener_zonas

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        # Incluye solo los campos relevantes
        fields = ['ciudad', 'tipo_propiedad', 'matricula_inmobiliaria', 'direccion', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        def clean(self):
            cleaned_data = super().clean()
            latitude = cleaned_data.get('latitude')
            longitude = cleaned_data.get('longitude')
            if latitude is None or longitude is None:
                raise forms.ValidationError("Debe seleccionar la ubicación en el mapa.")
            try:
                lat = float(latitude)
                lng = float(longitude)
            except (TypeError, ValueError):
                raise forms.ValidationError("Ubicación inválida. Seleccione un punto en el mapa.")
            return cleaned_data


class AgregarPropiedadClienteForm(forms.ModelForm):
    class Meta:
        model = PropiedadCliente
        fields = ['cliente', 'relacion']

    def __init__(self, *args, **kwargs):
        propiedad = kwargs.pop('propiedad', None)
        super().__init__(*args, **kwargs)
        if propiedad:
            # Excluir clientes ya asociados a esa propiedad
            clientes_asociados = propiedad.propiedadcliente_set.values_list('cliente_id', flat=True)
            self.fields['cliente'].queryset = Cliente.objects.exclude(id__in=clientes_asociados)


'''
Clase form para el estimador de metros cuadrados, que eventualmente va a ser un Agente AI
'''
class EstimadorForm(forms.Form):
    area_objetivo = forms.FloatField(label='Área del inmueble (m²)', min_value=1)
    id_country = forms.ChoiceField(label='País', choices=[], required=True)
    id_region = forms.ChoiceField(label='Región', choices=[], required=False)
    id_city = forms.ChoiceField(label='Ciudad', choices=[], required=False)
    id_location = forms.ChoiceField(label='Localidad', choices=[], required=False)
    id_zone = forms.ChoiceField(label='Zona', choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_country'].choices = obtener_paises()

        data = args[0] if args else {}

        id_country = data.get('id_country')
        if id_country:
            self.fields['id_region'].choices = obtener_regiones(id_country)

        id_region = data.get('id_region')
        if id_region:
            self.fields['id_city'].choices = obtener_ciudades(id_region)

        id_city = data.get('id_city')
        if id_city:
            self.fields['id_location'].choices = obtener_localidades(id_city)
            self.fields['id_zone'].choices = obtener_zonas(id_city)


'''
A partir de esta linea se hacen los forms para creación de formulario de entrega
'''

# class SeleccionarPropiedadClienteForm(forms.ModelForm):
#     class Meta:
#         model = PropiedadCliente
#         fields = ['propiedad', 'cliente', 'relacion']

class SeleccionarPropiedadClienteForm(forms.ModelForm):
    class Meta:
        model = PropiedadCliente
        fields = ['cliente']
    
    def __init__(self, *args, **kwargs):
        propiedad = kwargs.pop('propiedad', None)
        super().__init__(*args, **kwargs)
        if propiedad:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                propiedadcliente__propiedad=propiedad,
                propiedadcliente__relacion=PropiedadCliente.ARRENDATARIO
            ).distinct()
        else:
            self.fields['cliente'].queryset = Cliente.objects.none()


class AmbienteEntregaForm(forms.ModelForm):
    class Meta:
        model = AmbienteEntrega
        fields = ['tipo_ambiente', 'numero_ambiente', 'nombre_personalizado']


ItemEntregaFormSet = modelformset_factory(
    ItemEntrega,
    fields=['nombre_item', 'estado', 'cantidad', 'material', 'observaciones'],
    extra=0
)


'''
ModelForm para hacer la creación del formulario de captación
'''
class FormularioCaptacionDinamico(forms.ModelForm):
    class Meta:
        model = FormularioCaptacion
        fields = ['tipo_captacion', 'observaciones_generales']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secciones = []
        secciones = SeccionCaptacion.objects.prefetch_related('campos').order_by('orden')
        for seccion in secciones:
            campos_lista = []
            for campo in seccion.campos.all().order_by('orden'):
                field_name = f'campo_{campo.id}'
                campos_lista.append(field_name)
                if campo.tipo == 'texto':
                    self.fields[field_name] = forms.CharField(
                        label=campo.nombre,
                        required=campo.obligatorio
                    )
                elif campo.tipo == 'numero':
                    self.fields[field_name] = forms.FloatField(
                        label=campo.nombre,
                        required=campo.obligatorio
                    )
                elif campo.tipo == 'booleano':
                    self.fields[field_name] = forms.BooleanField(
                        label=campo.nombre,
                        required=False
                    )
            # Guardamos el nombre y los campos de la sección para el template
            self.secciones.append({'nombre': seccion.nombre, 'campos': campos_lista})
