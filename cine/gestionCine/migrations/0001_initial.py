# Generated by Django 3.1.4 on 2021-01-20 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('ID_Peli', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('duracion', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('detalle', models.TextField()),
                ('genero', models.CharField(max_length=50)),
                ('clasificacion', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('fechaComienzo', models.DateField(verbose_name='Fecha de comienzo')),
                ('fechaFinalizacion', models.DateField(verbose_name='Fecha de Finalizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Salas',
            fields=[
                ('ID_Sala', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=20)),
                ('fila', models.IntegerField()),
                ('asientos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('ID_Proye', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de finalizacion')),
                ('hora', models.TimeField()),
                ('estado', models.BooleanField(default=False)),
                ('pelicula', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionCine.pelicula')),
                ('sala', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionCine.salas')),
            ],
        ),
        migrations.CreateModel(
            name='Butacas',
            fields=[
                ('ID_butacas', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('fila', models.IntegerField()),
                ('asiento', models.IntegerField()),
                ('proyeccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionCine.proyeccion')),
            ],
        ),
    ]