# Generated by Django 3.1.4 on 2021-01-20 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCine', '0005_auto_20201210_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='duracion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='estado',
            field=models.CharField(max_length=50),
        ),
    ]
