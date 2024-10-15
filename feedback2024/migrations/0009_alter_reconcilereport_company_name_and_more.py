# Generated by Django 4.0.4 on 2024-09-01 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback2024', '0008_alter_whistleblower_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconcilereport',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reconcilereport',
            name='company_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reconcilereport',
            name='nssf_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reconcilereport',
            name='type',
            field=models.CharField(blank=True, choices=[('Statement issues', 'Statement issues'), ('Non Payment', 'Non Payment')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reconcilereport',
            name='work_from_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
