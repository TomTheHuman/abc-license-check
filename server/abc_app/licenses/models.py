from django.db import models
from django.db.models.fields import related

# TODO Need to update report import process to reflect report model with type

REPORT_TYPE_CHOICES = (
    ("status_change", "Status Change"),
    ("new_application", "New Application"),
    ("issued_license", "Issued License")
)


class Action(models.Model):
    code = models.CharField(primary_key=True, max_length=48, null=False)
    description = models.CharField(max_length=255, null=False)


class District(models.Model):
    code = models.IntegerField(primary_key=True, null=False)
    description = models.CharField(max_length=255, null=False)
    in_territory = models.BooleanField(default=False)


class Status(models.Model):
    code = models.CharField(primary_key=True, max_length=48, null=False)
    description = models.CharField(max_length=255, null=False)


class Recipient(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    email_address = models.EmailField(max_length=255, null=False, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class Admin(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    email_address = models.EmailField(max_length=255, null=False, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class Report(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(
        max_length=255, null=False, choices=REPORT_TYPE_CHOICES, default='status_change')
    lic_num = models.IntegerField(blank=True)
    status_from = models.ForeignKey(
        Status, on_delete=models.PROTECT, blank=True, null=True, related_name="status_from")
    status_to = models.ForeignKey(
        Status, on_delete=models.PROTECT, blank=True, null=True, related_name="status_to")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=True, null=True)
    lic_type = models.CharField(max_length=24, blank=True)
    lic_dup = models.CharField(max_length=24, blank=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    acct_name = models.CharField(max_length=255, blank=True, null=True)
    acct_own = models.CharField(max_length=255, blank=True, null=True)
    acct_street = models.CharField(max_length=255, blank=True, null=True)
    acct_city = models.CharField(max_length=255, blank=True, null=True)
    acct_state = models.CharField(max_length=8, blank=True, null=True)
    acct_zip = models.CharField(max_length=48, blank=True, null=True)
    mail_street = models.CharField(max_length=255, blank=True, null=True)
    mail_city = models.CharField(max_length=255, blank=True, null=True)
    mail_state = models.CharField(max_length=8, blank=True, null=True)
    mail_zip = models.CharField(max_length=48, blank=True, null=True)
    conditions = models.CharField(max_length=48, blank=True, null=True)
    escrow_addr = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, blank=True, null=True)
    trans_from = models.CharField(max_length=48, blank=True, null=True)
    trans_to = models.CharField(max_length=48, blank=True, null=True)
    geocode = models.IntegerField(blank=True, null=True)
