# Generated by Django 5.1.5 on 2025-02-20 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioapp', '0004_alter_formulariocaptacion_valor_renta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulariocaptacion',
            name='tipo_captacion',
            field=models.CharField(blank=True, choices=[('RE', 'Renta'), ('VE', 'Venta'), ('AM', 'Ambos')], max_length=2, null=True),
        ),
    ]
