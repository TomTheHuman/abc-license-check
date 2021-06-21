# Generated by Django 3.2.4 on 2021-06-21 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('district_code', models.IntegerField(primary_key=True, serialize=False)),
                ('district_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lic_num', models.IntegerField(max_length=100)),
                ('status', models.DateTimeField(blank=True)),
                ('lic_type', models.CharField(blank=True, max_length=24)),
                ('lic_dup', models.CharField(blank=True, max_length=24)),
                ('exp_date', models.DateTimeField(blank=True)),
                ('acct_name', models.CharField(blank=True, max_length=255)),
                ('acct_own', models.CharField(blank=True, max_length=255)),
                ('acct_street', models.CharField(blank=True, max_length=255)),
                ('acct_city', models.CharField(blank=True, max_length=255)),
                ('acct_state', models.CharField(blank=True, max_length=8)),
                ('acct_zip', models.CharField(blank=True, max_length=48)),
                ('mail_street', models.CharField(blank=True, max_length=255)),
                ('mail_city', models.CharField(blank=True, max_length=255)),
                ('mail_state', models.CharField(blank=True, max_length=8)),
                ('mail_zip', models.CharField(blank=True, max_length=48)),
                ('action', models.CharField(blank=True, max_length=48)),
                ('conditions', models.CharField(blank=True, max_length=48)),
                ('escrow_addr', models.CharField(blank=True, max_length=255)),
                ('district_code', models.IntegerField(blank=True)),
                ('geocode', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lic_num', models.IntegerField(max_length=100)),
                ('status', models.DateTimeField(blank=True)),
                ('lic_type', models.CharField(blank=True, max_length=24)),
                ('lic_dup', models.CharField(blank=True, max_length=24)),
                ('exp_date', models.DateTimeField(blank=True)),
                ('acct_name', models.CharField(blank=True, max_length=255)),
                ('acct_own', models.CharField(blank=True, max_length=255)),
                ('acct_street', models.CharField(blank=True, max_length=255)),
                ('acct_city', models.CharField(blank=True, max_length=255)),
                ('acct_state', models.CharField(blank=True, max_length=8)),
                ('acct_zip', models.CharField(blank=True, max_length=48)),
                ('mail_street', models.CharField(blank=True, max_length=255)),
                ('mail_city', models.CharField(blank=True, max_length=255)),
                ('mail_state', models.CharField(blank=True, max_length=8)),
                ('mail_zip', models.CharField(blank=True, max_length=48)),
                ('action', models.CharField(blank=True, max_length=48)),
                ('conditions', models.CharField(blank=True, max_length=48)),
                ('escrow_addr', models.CharField(blank=True, max_length=255)),
                ('district_code', models.IntegerField(blank=True)),
                ('geocode', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipients',
            fields=[
                ('username', models.EmailField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StatusChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lic_num', models.IntegerField(max_length=100)),
                ('status_from', models.DateTimeField(blank=True)),
                ('status_to', models.DateTimeField(blank=True)),
                ('lic_type', models.CharField(blank=True, max_length=24)),
                ('lic_dup', models.CharField(blank=True, max_length=24)),
                ('issue_date', models.DateTimeField(blank=True)),
                ('exp_date', models.DateTimeField(blank=True)),
                ('acct_name', models.CharField(blank=True, max_length=255)),
                ('acct_own', models.CharField(blank=True, max_length=255)),
                ('acct_street', models.CharField(blank=True, max_length=255)),
                ('acct_city', models.CharField(blank=True, max_length=255)),
                ('acct_state', models.CharField(blank=True, max_length=8)),
                ('acct_zip', models.CharField(blank=True, max_length=48)),
                ('mail_street', models.CharField(blank=True, max_length=255)),
                ('mail_city', models.CharField(blank=True, max_length=255)),
                ('mail_state', models.CharField(blank=True, max_length=8)),
                ('mail_zip', models.CharField(blank=True, max_length=48)),
                ('trans_from', models.CharField(blank=True, max_length=48)),
                ('trans_to', models.CharField(blank=True, max_length=48)),
                ('geocode', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('status_code', models.CharField(max_length=48, primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=255)),
            ],
        ),
    ]
