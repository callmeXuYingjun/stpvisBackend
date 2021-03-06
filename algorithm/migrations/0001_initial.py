# Generated by Django 3.0.2 on 2020-01-27 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('a0', models.FloatField()),
                ('a1', models.FloatField()),
                ('a2', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=50)),
                ('upwd', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]
