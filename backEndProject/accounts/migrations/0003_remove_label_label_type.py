# Generated by Django 4.0.2 on 2022-03-30 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='label_type',
        ),
    ]
