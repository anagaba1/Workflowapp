# Generated by Django 4.0.4 on 2024-08-31 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback2024', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whistleblower',
            name='number_employees',
            field=models.CharField(max_length=255),
        ),
    ]
