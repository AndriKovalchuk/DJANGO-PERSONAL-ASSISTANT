# Generated by Django 5.0.4 on 2024-05-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.CharField(),
        ),
    ]
