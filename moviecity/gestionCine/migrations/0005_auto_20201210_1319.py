# Generated by Django 3.1.4 on 2020-12-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCine', '0004_auto_20201210_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='butacas',
            name='ID_butacas',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='ID_Peli',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='proyeccion',
            name='ID_Proye',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='salas',
            name='ID_Sala',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
