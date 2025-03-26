from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('No puede contener caracteres, solo números')

class Ciudad(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre

class TipoPropiedad(models.Model):
    tipo_propiedad = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo_propiedad

    class Meta:
        ordering = ['tipo_propiedad']
        verbose_name = 'Tipo de Propiedades'
        verbose_name_plural = 'Tipos de Propiedades'


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    identificacion = models.CharField(max_length=200,
                                      validators=[only_int],
                                      blank=True,null=True,
                                      unique=True)
    direccion_correspondiencia = models.CharField(max_length=200,blank=True,null=True)
    telefono = models.CharField(max_length=200,blank=True,null=True,validators=[only_int])
    email = models.EmailField(max_length=254,blank=True,null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre

class Propiedad(models.Model):
    ciudad = models.ForeignKey(Ciudad,related_name='ciudad_propiedad',
                                         blank=True,
                                         on_delete=models.DO_NOTHING)
    tipo_propiedad = models.ForeignKey(TipoPropiedad,related_name='propiedad_tipo',
                                         on_delete=models.DO_NOTHING)
    matricula_inmobiliaria= models.CharField(max_length=200,blank=True,null=True)
    direccion= models.CharField(max_length=200)
    clientes = models.ManyToManyField(Cliente,
                                     through='PropiedadCliente',
                                     related_name='clientes_propiedad')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    
    def __str__(self):
        return self.direccion

class PropiedadCliente(models.Model):
    # Se definen las opciones de tipo de relación entre cliente y propiedad
    PROPIETARIO = 'PR'
    APODERADO = 'AP'
    ARRENDATARIO = 'AR'
    TipoRelacion={
        PROPIETARIO : 'Propietario',
        APODERADO : 'Apoderado',
        ARRENDATARIO : 'Arrendatario'
    }
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    relacion = models.CharField(max_length=2,
                              choices=TipoRelacion)
    
    class Meta:
        verbose_name = 'Propiedades y Clientes'
        verbose_name_plural = 'Propiedades y Clientes'

    def __str__(self):
        return f'El cliente {self.cliente} es {self.get_relacion_display()} de la {self.propiedad}'

'''
MODELO INICIAL, PEDIENTE POR TERMINAR 
'''
class FormularioCaptacion(models.Model):
    # Se definen los tipos de captación
    RENTA = 'RE'
    VENTA = 'VE'
    AMBOS = 'AM'
    TipoCaptacion={
        RENTA : 'Renta',
        VENTA : 'Venta',
        AMBOS : 'Ambos'
    }
    fecha = models.DateTimeField()
    tipo_captacion = models.CharField(max_length=2,
                              choices=TipoCaptacion,null=True,blank=True)
    valor_venta = models.DecimalField(max_digits = 13,decimal_places=2,null=True,blank=True)
    valor_renta = models.DecimalField(max_digits = 13,decimal_places=2,null=True,blank=True)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Formulario de Captación'
        verbose_name_plural = 'Formularios de Captación'

class DetallePropiedad(models.Model):
    NUMERO = 'NU'
    TEXTO = 'TE'
    SINO = 'SN'
    TipoCampo={
        NUMERO : 'Número',
        TEXTO : 'Texto',
        SINO : 'Si/No'
    }
    GENERAL = 'GN'
    INTERIOR = 'IN'
    EXTERIOR = 'EX'
    TipoDetalle={
        GENERAL : 'General',
        INTERIOR : 'Interior',
        EXTERIOR : 'Exterior'
    }
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200,blank=True,null=True)
    tipo_campo = models.CharField(max_length=2,
                              choices=TipoCampo)
    tipo_detalle = models.CharField(max_length=2,
                              choices=TipoDetalle)
    clase_propiedad = models.ManyToManyField(TipoPropiedad, blank=True)

    class Meta:
        verbose_name = 'Detalle de Propiedad'
        verbose_name_plural = 'Detalles de Propiedad'

    def __str__(self):
        return self.nombre

class DetalleCaptacion(models.Model):
    detalle = models.CharField(max_length=200,blank=True,null=True)
    detalle_propiedad = models.ForeignKey(DetallePropiedad, on_delete=models.DO_NOTHING)
    formulario_captacion = models.ForeignKey(FormularioCaptacion, on_delete=models.CASCADE)


'''
MODELO ALTERNATIVO
'''

class AltDetallesExteriores(models.Model):
    SI = 'SI'
    NO = 'NO'
    TipoCampoSiNo={
        SI : 'Si',
        NO : 'No'
    }
    formulario_captacion = models.OneToOneField(FormularioCaptacion, on_delete=models.CASCADE,default=0)
    jacuzzi = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    cancha_multiple = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Cancha Múltiple')
    zona_bbq = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Zona BBQ')
    turco = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    sauna = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    espejo_de_agua = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    vigilancia = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    terraza = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    zona_infantil = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    vista_panoramica = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Vista Panorámica')
    salon_de_juegos = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    sala_de_internet = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    planta_electrica = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Planta Eléctrica')
    parqueadero_visitantes = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    cuarto_de_escoltas = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    salon_comunal = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    oficina_de_negocios = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    espacio_de_golf = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    circuito_cerrado_de_tv = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Circuito Cerrado de TV')
    cancha_de_tenis = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    jardin = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Jardín')
    caldera = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    gimnasio = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    zonas_verdes = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    piscina = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    ascensor = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    conjunto_cerrado = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Detalles Exteriores Formulario de Captación'
        verbose_name_plural = 'Detalles Exteriores Formulario de Captación'
    
    def __str__(self):
        return f'{self.formulario_captacion}'


class AltDetallesInteriores(models.Model):
    SI = 'SI'
    NO = 'NO'
    TipoCampoSiNo={
        SI : 'Si',
        NO : 'No'
    }
    formulario_captacion = models.OneToOneField(FormularioCaptacion, on_delete=models.CASCADE,default=0)
    closets = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    vestier = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    turco = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    jacuzzi = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    zona_de_lavanderia = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    tipo_de_piso = models.CharField(max_length=100,
                              null=True,blank=True)
    sauna = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    patio = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    cocina_integral = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    hall_de_alcobas = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    cuarto_de_servicio = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    deposito = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    estudio = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    comedor_auxiliar = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    cocina_tipo_americano = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    tipo_instalacion_de_gas = models.CharField(max_length=100,
                              null=True,blank=True,verbose_name='Tipo de Instalación de Gas')
    citofono = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Citófono')
    chimenea = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    calentador = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    barra_estilo_americano = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    banio_auxiliar = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Baño Auxiliar')
    balcon = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True,verbose_name='Balcón')
    amoblado = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    alarma = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    aire_acondicionado = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    otros_u_observaciones = models.TextField(blank=True,null=True)
    
    class Meta:
        verbose_name = 'Detalles Interiores Formulario de Captación'
        verbose_name_plural = 'Detalles Interiores Formulario de Captación'
    
    def __str__(self):
        return f'{self.formulario_captacion}'
    
class AltDetallesGenerales(models.Model):
    SI = 'SI'
    NO = 'NO'
    TipoCampoSiNo={
        SI : 'Si',
        NO : 'No'
    }
    NUEVO = 'NU'
    USADO = 'US'
    TipoEstadoNuevoUsado={
        NUEVO : 'Nuevo',
        USADO : 'Usado'
    }
    formulario_captacion = models.OneToOneField(FormularioCaptacion, on_delete=models.CASCADE,default=0)
    parqueadero_cubierto = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    parqueaderos = models.IntegerField(blank=True,null=True)
    valor_gravamen = models.BigIntegerField(blank=True,null=True)
    gravamen = models.CharField(max_length=2,
                              choices=TipoCampoSiNo,null=True,blank=True)
    estado_nuevo_usado = models.CharField(max_length=2,
                              choices=TipoEstadoNuevoUsado,null=True,blank=True,verbose_name='Nuevo/Usado')
    cantidad_banios = models.IntegerField(blank=True,null=True,verbose_name='Cantidad de Baños')
    numero_piso = models.IntegerField(blank=True,null=True,verbose_name='Número de Piso')
    estado = models.CharField(max_length=200,null=True,blank=True)
    anios_construido = models.IntegerField(blank=True,null=True,verbose_name='Años Construido')
    valor_administracion = models.BigIntegerField(blank=True,null=True)
    cantidad_habitaciones = models.IntegerField(blank=True,null=True)
    area_privada = models.IntegerField(blank=True,null=True,verbose_name='Área Privada')
    area = models.IntegerField(blank=True,null=True,verbose_name='Área')
    estrato = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)],blank=True,null=True)
    

    class Meta:
        verbose_name = 'Detalles Generales Formulario de Captación'
        verbose_name_plural = 'Detalles Generales Formulario de Captación'
    
    def __str__(self):
        return f'{self.formulario_captacion}'

