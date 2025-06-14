# Generated by Django 5.1.5 on 2025-03-10 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioapp', '0011_altformulariocaptacion_altdetallesinteriores_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='altdetallesexteriores',
            name='alt_formulario_captacion',
        ),
        migrations.RemoveField(
            model_name='altdetallesgenerales',
            name='alt_formulario_captacion',
        ),
        migrations.RemoveField(
            model_name='altdetallesinteriores',
            name='alt_formulario_captacion',
        ),
        migrations.AddField(
            model_name='altdetallesexteriores',
            name='formulario_captacion',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='inventarioapp.formulariocaptacion'),
        ),
        migrations.AddField(
            model_name='altdetallesgenerales',
            name='formulario_captacion',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='inventarioapp.formulariocaptacion'),
        ),
        migrations.AddField(
            model_name='altdetallesinteriores',
            name='formulario_captacion',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='inventarioapp.formulariocaptacion'),
        ),
        migrations.DeleteModel(
            name='AltFormularioCaptacion',
        ),
    ]
