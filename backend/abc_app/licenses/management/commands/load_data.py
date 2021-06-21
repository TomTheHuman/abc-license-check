from csv import DictReader
from datetime import datetime
from typing import Dict
from django.core.management import BaseCommand

from licenses.models import StatusChange, NewApplication, IssuedLicense, Actions, Districts, Statuses, Recipients
from pytz import UTC

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for row in DictReader(open('./licenses/import/action.csv')):
            action = Actions()
            print(row['action_code'])
            action.action_code = row['action_code']
            action.action_name = row['action_name']
            action.save()

        for row in DictReader(open('./licenses/import/district_codes.csv')):
            district = Districts()
            print(row['district_code'])
            district.district_code = row['district_code']
            district.district_name = row['district_name']
            district.save()

        for row in DictReader(open('./licenses/import/recipients.csv')):
            recipient = Recipients()
            recipient.username = row['username']
            recipient.first_name = row['first_name']
            recipient.last_name = row['last_name']
            recipient.save()

        for row in DictReader(open('./licenses/import/status.csv')):
            status = Statuses()
            status.status_code = row['status_code']
            status.status_name = row['status_name']
            status.save()