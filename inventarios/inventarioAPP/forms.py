from django import forms
from django.forms import modelformset_factory
from .models import *
from django.forms.formsets import Form, BaseFormSet, formset_factory, ValidationError
from .wasi_api import obtener_paises, obtener_regiones, obtener_ciudades, obtener_localidades, obtener_zonas

class CaptacionForm(forms.ModelForm):
    # fecha = forms.DateTimeField(label='Fecha de Captación', widget=forms.DateTimeInput)
    class Meta:
        model = FormularioCaptacion
        fields = ['fecha','tipo_captacion','valor_venta','valor_renta']
        widgets = {
            'fecha':forms.TextInput(attrs={'type':'datetime-local'}),
        }

class detallesGeneralesCaptacionForm(forms.ModelForm):
    class Meta:
        model = AltDetallesGenerales
        fields = '__all__'
        exclude = ('formulario_captacion',)

class detallesExterioresCaptacionForm(forms.ModelForm):
    class Meta:
        model = AltDetallesExteriores
        fields = '__all__'
        exclude = ('formulario_captacion',)

class detallesInterioresCaptacionForm(forms.ModelForm):
    class Meta:
        model = AltDetallesInteriores
        fields = '__all__'
        exclude = ('formulario_captacion',)


class detalleCaptacionForm(forms.Form):
    detalle = forms.CharField(max_length=100)


# Clase form para el estimador de metros cuadrados, que eventualmente va a ser un Agente AI
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

class SeleccionarPropiedadClienteForm(forms.ModelForm):
    class Meta:
        model = PropiedadCliente
        fields = ['propiedad', 'cliente', 'relacion']

class AmbienteEntregaForm(forms.ModelForm):
    class Meta:
        model = AmbienteEntrega
        fields = ['tipo_ambiente', 'numero_ambiente', 'nombre_personalizado']


ItemEntregaFormSet = modelformset_factory(
    ItemEntrega,
    fields=['nombre_item', 'estado', 'cantidad', 'material', 'observaciones'],
    extra=0
)