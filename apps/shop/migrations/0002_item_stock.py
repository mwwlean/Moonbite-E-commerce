# Generated by Django 4.2.6 on 2024-07-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
