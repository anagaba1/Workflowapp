# Generated by Django 4.0.4 on 2024-04-06 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0032_alter_jotfeedback_fcr_resolved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jotfeedback',
            name='ces_easy',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='jotfeedback',
            name='overall_satisfaction',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, null=True),
        ),
    ]
