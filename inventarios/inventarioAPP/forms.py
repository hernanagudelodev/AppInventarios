from django import forms
from .models import FormularioCaptacion,AltDetallesExteriores,AltDetallesGenerales,AltDetallesInteriores
from django.forms.formsets import Form, BaseFormSet, formset_factory, ValidationError

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
# class detalleCaptacionFormSet(forms.Form,detalleCaptacion):
#     for 