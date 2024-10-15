# Generated by Django 4.0.4 on 2023-07-19 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0006_remove_engagementlog_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engagementlog',
            name='modified_at',
        ),
        migrations.AddField(
            model_name='engagement',
            name='modified_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='engagementlog',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
