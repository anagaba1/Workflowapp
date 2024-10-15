# Generated by Django 4.0.4 on 2024-03-02 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowapp', '0020_feedback4_additional_comments_feedback4_ces_easy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traffic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_date', models.DateField()),
                ('nssf_number', models.CharField(max_length=20)),
                ('channel', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('reason', models.TextField()),
                ('served_by', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
    ]
