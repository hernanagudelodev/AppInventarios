# Generated by Django 5.1.5 on 2025-05-15 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioapp', '0012_remove_altdetallesexteriores_alt_formulario_captacion_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='altdetallesexteriores',
            options={'verbose_name': 'Detalles Exteriores Formulario de Captación', 'verbose_name_plural': 'Detalles Exteriores Formulario de Captación'},
        ),
        migrations.AlterModelOptions(
            name='altdetallesgenerales',
            options={'verbose_name': 'Detalles Generales Formulario de Captación', 'verbose_name_plural': 'Detalles Generales Formulario de Captación'},
        ),
        migrations.AlterModelOptions(
            name='altdetallesinteriores',
            options={'verbose_name': 'Detalles Interiores Formulario de Captación', 'verbose_name_plural': 'Detalles Interiores Formulario de Captación'},
        ),
    ]
