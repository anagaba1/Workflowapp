# Generated by Django 4.0.4 on 2024-09-24 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback2024', '0021_rename_whistleblowerlog_attachment_whistleblowerlog_case'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='whistleblowerLog_case',
            new_name='whistleblowerLog',
        ),
    ]
