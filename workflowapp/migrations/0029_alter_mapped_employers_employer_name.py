# Generated by Django 4.0.4 on 2024-03-07 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0028_mapped_employers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapped_employers',
            name='employer_name',
            field=models.CharField(max_length=300),
        ),
    ]
