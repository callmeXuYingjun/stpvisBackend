# Generated by Django 3.0 on 2019-12-10 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm', '0003_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]