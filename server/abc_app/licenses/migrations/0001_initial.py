# Generated by Django 3.2.5 on 2021-07-10 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('code', models.CharField(max_length=48, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email_address', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('in_territory', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email_address', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('code', models.CharField(max_length=48, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('report_type', models.CharField(choices=[('status_change', 'Status Change'), ('new_application', 'New Application'), ('issued_license', 'Issued License')], default='status_change', max_length=255)),
                ('lic_num', models.IntegerField(blank=True)),
                ('lic_type', models.CharField(blank=True, max_length=24)),
                ('lic_dup', models.CharField(blank=True, max_length=24)),
                ('issue_date', models.DateTimeField(blank=True, null=True)),
                ('exp_date', models.DateTimeField(blank=True, null=True)),
                ('acct_name', models.CharField(blank=True, max_length=255, null=True)),
                ('acct_own', models.CharField(blank=True, max_length=255, null=True)),
                ('acct_street', models.CharField(blank=True, max_length=255, null=True)),
                ('acct_city', models.CharField(blank=True, max_length=255, null=True)),
                ('acct_state', models.CharField(blank=True, max_length=8, null=True)),
                ('acct_zip', models.CharField(blank=True, max_length=48, null=True)),
                ('mail_street', models.CharField(blank=True, max_length=255, null=True)),
                ('mail_city', models.CharField(blank=True, max_length=255, null=True)),
                ('mail_state', models.CharField(blank=True, max_length=8, null=True)),
                ('mail_zip', models.CharField(blank=True, max_length=48, null=True)),
                ('conditions', models.CharField(blank=True, max_length=48, null=True)),
                ('escrow_addr', models.CharField(blank=True, max_length=255, null=True)),
                ('trans_from', models.CharField(blank=True, max_length=48, null=True)),
                ('trans_to', models.CharField(blank=True, max_length=48, null=True)),
                ('geocode', models.IntegerField(blank=True, null=True)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='licenses.district')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='licenses.status')),
                ('status_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status_from', to='licenses.status')),
                ('status_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status_to', to='licenses.status')),
            ],
        ),
    ]
