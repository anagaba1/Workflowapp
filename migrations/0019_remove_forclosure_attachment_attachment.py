# Generated by Django 4.0.4 on 2023-06-05 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0018_remove_forclosure_attachments_forclosure_attachment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forclosure',
            name='attachment',
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('forclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='workflowapp.forclosure')),
            ],
        ),
    ]
