# Generated by Django 5.1.3 on 2024-12-15 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelaje', '0006_areacomparacion_peso_decisionalternative_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='areacomparacion',
            name='symbol',
            field=models.CharField(default='*', max_length=1),
        ),
    ]
