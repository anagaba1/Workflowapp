# Generated by Django 4.0.4 on 2024-03-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0017_getfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
    ]
