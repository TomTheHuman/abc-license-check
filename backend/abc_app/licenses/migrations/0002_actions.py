# Generated by Django 3.2.4 on 2021-06-21 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('action_code', models.CharField(max_length=48, primary_key=True, serialize=False)),
                ('action_name', models.CharField(max_length=255)),
            ],
        ),
    ]