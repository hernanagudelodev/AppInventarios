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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

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
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'propiedad', 'relacion'], name='unique_cliente_propiedad_relacion')
        ]

    def __str__(self):
        return f'El cliente {self.cliente} es {self.get_relacion_display()} de la {self.propiedad}'


'''
Formulario de entrega.
A partir de esta linea se crea el formulario de entrega y sus clases necesarias
'''

'''
Este es el modelo de formulario de entrega, que tiene la parte inicial de este formulario.
Se relaciona con propiedadCliente, que tiene la relación entre un cliente y una propiedad.'''
class FormularioEntrega(models.Model):
    propiedad_cliente = models.ForeignKey(PropiedadCliente, on_delete=models.CASCADE)
    fecha_entrega = models.DateField(auto_now_add=True)
    observaciones_generales = models.TextField(blank=True, null=True)
    firma_cliente = models.ImageField(upload_to='firmas/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    is_firmado = models.BooleanField(default=False)
    fecha_firma = models.DateTimeField(null=True, blank=True)

    @property
    def propiedad(self):
        return self.propiedad_cliente.propiedad

    class Meta:
        verbose_name = 'Formulario de Entrega'
        verbose_name_plural = 'Formularios de Entrega'
        ordering = ['-creado']

    def __str__(self):
        return f'Entrega de {self.propiedad_cliente.propiedad} a {self.propiedad_cliente.cliente}'


'''
Esta clase define la plantilla para items, dependiendo del tipo de ambiente.
Va a permitir que al crear el formulario, e ir agregando tipos de ambiente, se 
creen automaticamente los items de ese ambiente de acuerdo a esta base.
'''
class ItemBase(models.Model):
    TIPO_AMBIENTE_CHOICES = [
        ('ALCOBA', 'Alcoba'),
        ('BAÑO', 'Baño'),
        ('COCINA', 'Cocina'),
        ('SALA', 'Sala'),
        ('COMEDOR', 'Comedor'),
        ('ZONA_ROPA', 'Zona de Ropa'),
        ('BALCON', 'Balcón'),
        ('OTRO', 'Otro'),
    ]

    tipo_ambiente = models.CharField(max_length=20, choices=TIPO_AMBIENTE_CHOICES)
    nombre_item = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Item Base'
        verbose_name_plural = 'Items Base'
        unique_together = ('tipo_ambiente', 'nombre_item')

    def __str__(self):
        return f'{self.nombre_item} ({self.get_tipo_ambiente_display()})'


'''
Esta clase tiene los item de entrega de un ambiente especifico, de un formulario especifico.
Se copia una parte de item base, según el tipo de ambiente, y deja espacio para crear items
personalizados
'''
class ItemEntrega(models.Model):
    ESTADO_CHOICES = [
        ('B', 'Bueno'),
        ('R', 'Regular'),
        ('M', 'Malo'),
    ]

    ambiente_entrega = models.ForeignKey('AmbienteEntrega', on_delete=models.CASCADE, related_name='items')
    nombre_item = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    es_personalizado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre_item} - {self.get_estado_display()}'


'''
Clase que define los diferentes ambientes de entrega: alcoba o habitación, baño, cocina, etc.
'''
class AmbienteEntrega(models.Model):
    TIPO_AMBIENTE_CHOICES = ItemBase.TIPO_AMBIENTE_CHOICES

    formulario_entrega = models.ForeignKey(FormularioEntrega, on_delete=models.CASCADE, related_name='ambientes')
    tipo_ambiente = models.CharField(max_length=20, choices=TIPO_AMBIENTE_CHOICES)
    numero_ambiente = models.PositiveIntegerField(blank=True, null=True)
    nombre_personalizado = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.get_tipo_ambiente_display()} #{self.numero_ambiente or ""}'

    '''
    Hook automático de creación de ítems estándar al crear un nuevo ambiente.
    
    Este método sobrescribe `save()` para detectar si el ambiente es nuevo (pk aún no existe).
    Si es nuevo, consulta la tabla ItemBase y trae todos los ítems asociados al tipo de ambiente.
    Luego, crea automáticamente instancias de ItemEntrega para ese ambiente, replicando cada ítem base.

    Ejemplo: al crear un ambiente de tipo "Baño", si en ItemBase están definidos los ítems
    "Inodoro", "Lavamanos" y "Espejo" para baños, entonces esos tres ítems serán creados
    automáticamente como parte del nuevo ambiente.
    
    Esto mejora la usabilidad, reduce errores manuales y estandariza el contenido de los formularios.
    '''

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            plantilla = ItemBase.objects.filter(tipo_ambiente=self.tipo_ambiente)
            for item in plantilla:
                ItemEntrega.objects.create(
                    ambiente_entrega=self,
                    nombre_item=item.nombre_item,
                    estado='B'  #valor por defecto
                )
    


'''
INVENTARIO DE CAPTACIÓN
A partir de esta linea se hace la V2 del modelo de captación, el cual permite configurar los items del inventario de captación
'''
'''
Esta clase define la sección del formulario de captación.'''
class SeccionCaptacion(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = "Sección de Captación"
        verbose_name_plural = "Secciones de Captación"

    def __str__(self):
        return self.nombre


'''
Esta clase define cada campo del inventario de captación
'''
class CampoCaptacion(models.Model):
    TIPO_CAMPO_CHOICES = [
        ('texto', 'Texto'),
        ('numero', 'Número'),
        ('booleano', 'Sí/No'),
    ]
    seccion = models.ForeignKey(SeccionCaptacion, on_delete=models.CASCADE, related_name='campos')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CAMPO_CHOICES)
    orden = models.PositiveIntegerField(default=0)
    obligatorio = models.BooleanField(default=False)

    class Meta:
        ordering = ['seccion', 'orden', 'id']
        verbose_name = "Campo de Captación"
        verbose_name_plural = "Campos de Captación"

    def __str__(self):
        return f"{self.seccion.nombre} - {self.nombre}"


'''
Clase de formulario de captación
'''
class FormularioCaptacion(models.Model):
    TIPO_CAPTACION_CHOICES = (
        ('venta', 'Venta'),
        ('renta', 'Renta'),
    )
    propiedad_cliente = models.ForeignKey(PropiedadCliente, on_delete=models.CASCADE, related_name='captaciones')
    fecha = models.DateField(auto_now_add=True)
    observaciones_generales = models.TextField(blank=True, null=True)
    firma_cliente = models.ImageField(upload_to='firmas_captacion/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    is_firmado = models.BooleanField(default=False)
    fecha_firma = models.DateTimeField(null=True, blank=True)
    tipo_captacion = models.CharField(max_length=10, choices=TIPO_CAPTACION_CHOICES)
    @property
    def propiedad(self):
        return self.propiedad_cliente.propiedad

    @property
    def cliente(self):
        return self.propiedad_cliente.cliente

    class Meta:
        ordering = ['-creado']
        verbose_name = "Formulario de Captación"
        verbose_name_plural = "Formularios de Captación"

    def __str__(self):
        return f'Captación de {self.propiedad} por {self.cliente} - {self.fecha}'

'''
Clase que define el valor de un campo de captación en un formulario de captación
'''
class ValorCampoCaptacion(models.Model):
    formulario = models.ForeignKey(FormularioCaptacion, on_delete=models.CASCADE, related_name='valores')
    campo = models.ForeignKey(CampoCaptacion, on_delete=models.CASCADE)
    valor_texto = models.TextField(blank=True, null=True)
    valor_numero = models.FloatField(blank=True, null=True)
    valor_booleano = models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together = ('formulario', 'campo')
        verbose_name = "Valor de Campo de Captación"
        verbose_name_plural = "Valores de Campos de Captación"

    def __str__(self):
        return f"{self.formulario} - {self.campo.nombre}"

