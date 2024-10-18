# Generated by Django 4.0.4 on 2023-06-02 06:47

from django.db import migrations, models
import workflowapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0006_alter_forclosure_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forclosure',
            name='attachment',
            field=models.FileField(default=workflowapp.models.get_default_attachment, upload_to='attachments/'),
        ),
    ]
