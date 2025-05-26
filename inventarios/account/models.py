from django.db import models # type: ignore
from django.conf import settings


class Inmobiliaria(models.Model):
    nombre = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos_inmobiliarias/', blank=True, null=True)
    texto_contractual_captacion_venta = models.TextField(default="Texto contractual de captación para venta por defecto...")
    texto_contractual_captacion_renta = models.TextField(default="Texto contractual de captación para renta por defecto...")
    texto_contractual_entrega = models.TextField(default="Texto contractual por defecto...")
    firma_autorizada = models.ImageField(upload_to='firmas_inmobiliarias/', blank=True, null=True)
    nombre_firma_autorizada = models.CharField(max_length=150, blank=True, help_text="Nombre del representante autorizado que firma")
    cedula_firma_autorizada = models.CharField(max_length=30, blank=True, help_text="Cédula o documento de identidad")
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d',blank=True)
    inmobiliaria = models.ForeignKey(Inmobiliaria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


# Create your models here.
