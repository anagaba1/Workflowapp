# Generated by Django 4.0.4 on 2024-04-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fliteracyapp', '0007_alter_attachment_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fl_attendants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nssf_number', models.CharField(max_length=20)),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateField()),
            ],
        ),
    ]
