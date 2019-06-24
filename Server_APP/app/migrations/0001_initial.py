# Generated by Django 2.0.4 on 2019-06-23 20:09

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('sinopsis', models.TextField(null=True)),
                ('poster', models.ImageField(null=True, upload_to='media/')),
                ('fechaEstreno', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resena', models.TextField(default='0')),
                ('idPelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pelicula')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=70)),
                ('contrasena', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='resena',
            name='idUsuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Usuario'),
        ),
    ]
