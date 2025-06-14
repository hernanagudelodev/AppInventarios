# Generated by Django 5.1.5 on 2025-05-19 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioapp', '0013_alter_altdetallesexteriores_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormularioEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega', models.DateField(auto_now_add=True)),
                ('observaciones_generales', models.TextField(blank=True, null=True)),
                ('firma_cliente', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('propiedad_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventarioapp.propiedadcliente')),
            ],
            options={
                'verbose_name': 'Formulario de Entrega',
                'verbose_name_plural': 'Formularios de Entrega',
                'ordering': ['-creado'],
            },
        ),
        migrations.CreateModel(
            name='AmbienteEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ambiente', models.CharField(choices=[('ALCOBA', 'Alcoba'), ('BAÑO', 'Baño'), ('COCINA', 'Cocina'), ('SALA', 'Sala'), ('COMEDOR', 'Comedor'), ('ZONA_ROPA', 'Zona de Ropa'), ('BALCON', 'Balcón'), ('OTRO', 'Otro')], max_length=20)),
                ('numero_ambiente', models.PositiveIntegerField(blank=True, null=True)),
                ('nombre_personalizado', models.CharField(blank=True, max_length=100, null=True)),
                ('formulario_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ambientes', to='inventarioapp.formularioentrega')),
            ],
        ),
        migrations.CreateModel(
            name='ItemBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ambiente', models.CharField(choices=[('ALCOBA', 'Alcoba'), ('BAÑO', 'Baño'), ('COCINA', 'Cocina'), ('SALA', 'Sala'), ('COMEDOR', 'Comedor'), ('ZONA_ROPA', 'Zona de Ropa'), ('BALCON', 'Balcón'), ('OTRO', 'Otro')], max_length=20)),
                ('nombre_item', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Item Base',
                'verbose_name_plural': 'Items Base',
                'unique_together': {('tipo_ambiente', 'nombre_item')},
            },
        ),
        migrations.CreateModel(
            name='ItemEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_item', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('B', 'Bueno'), ('R', 'Regular'), ('M', 'Malo')], max_length=1)),
                ('cantidad', models.PositiveIntegerField(blank=True, null=True)),
                ('material', models.CharField(blank=True, max_length=100, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('es_personalizado', models.BooleanField(default=False)),
                ('ambiente_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventarioapp.ambienteentrega')),
            ],
        ),
    ]
