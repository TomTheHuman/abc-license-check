from django.db import models

class StatusChange(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    lic_num = models.IntegerField(null=False)
    status_from = models.DateTimeField(blank=True);
    status_to = models.DateTimeField(blank=True);
    lic_type = models.CharField(max_length=24, blank=True);
    lic_dup = models.CharField(max_length=24, blank=True);
    issue_date = models.DateTimeField(blank=True);
    exp_date = models.DateTimeField(blank=True);
    acct_name = models.CharField(max_length=255, blank=True);
    acct_own = models.CharField(max_length=255, blank=True);
    acct_street = models.CharField(max_length=255, blank=True);
    acct_city = models.CharField(max_length=255, blank=True);
    acct_state = models.CharField(max_length=8, blank=True);
    acct_zip = models.CharField(max_length=48, blank=True);
    mail_street = models.CharField(max_length=255, blank=True);
    mail_city = models.CharField(max_length=255, blank=True);
    mail_state = models.CharField(max_length=8, blank=True);
    mail_zip = models.CharField(max_length=48, blank=True);
    trans_from = models.CharField(max_length=48, blank=True);
    trans_to = models.CharField(max_length=48, blank=True);
    geocode = models.IntegerField(blank=True);


class NewApplication(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    lic_num = models.IntegerField(null=False)
    status = models.DateTimeField(blank=True);
    lic_type = models.CharField(max_length=24, blank=True);
    lic_dup = models.CharField(max_length=24, blank=True);
    exp_date = models.DateTimeField(blank=True);
    acct_name = models.CharField(max_length=255, blank=True);
    acct_own = models.CharField(max_length=255, blank=True);
    acct_street = models.CharField(max_length=255, blank=True);
    acct_city = models.CharField(max_length=255, blank=True);
    acct_state = models.CharField(max_length=8, blank=True);
    acct_zip = models.CharField(max_length=48, blank=True);
    mail_street = models.CharField(max_length=255, blank=True);
    mail_city = models.CharField(max_length=255, blank=True);
    mail_state = models.CharField(max_length=8, blank=True);
    mail_zip = models.CharField(max_length=48, blank=True);
    action = models.CharField(max_length=48, blank=True);
    conditions = models.CharField(max_length=48, blank=True);
    escrow_addr = models.CharField(max_length=255, blank=True);
    district_code = models.IntegerField(blank=True);
    geocode = models.IntegerField(blank=True);


class IssuedLicense(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    lic_num = models.IntegerField(null=False)
    status = models.DateTimeField(blank=True);
    lic_type = models.CharField(max_length=24, blank=True);
    lic_dup = models.CharField(max_length=24, blank=True);
    exp_date = models.DateTimeField(blank=True);
    acct_name = models.CharField(max_length=255, blank=True);
    acct_own = models.CharField(max_length=255, blank=True);
    acct_street = models.CharField(max_length=255, blank=True);
    acct_city = models.CharField(max_length=255, blank=True);
    acct_state = models.CharField(max_length=8, blank=True);
    acct_zip = models.CharField(max_length=48, blank=True);
    mail_street = models.CharField(max_length=255, blank=True);
    mail_city = models.CharField(max_length=255, blank=True);
    mail_state = models.CharField(max_length=8, blank=True);
    mail_zip = models.CharField(max_length=48, blank=True);
    action = models.CharField(max_length=48, blank=True);
    conditions = models.CharField(max_length=48, blank=True);
    escrow_addr = models.CharField(max_length=255, blank=True);
    district_code = models.IntegerField(blank=True);
    geocode = models.IntegerField(blank=True);

class Actions(models.Model):
    action_code = models.CharField(primary_key=True, max_length=48, null=False)
    action_name = models.CharField(max_length=255, null=False)

class Districts(models.Model):
    district_code = models.IntegerField(primary_key=True, null=False)
    district_name = models.CharField(max_length=255, null=False)


class Statuses(models.Model):
    status_code = models.CharField(primary_key=True, max_length=48, null=False)
    status_name = models.CharField(max_length=255, null=False)


class Recipients(models.Model):
    username = models.EmailField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)