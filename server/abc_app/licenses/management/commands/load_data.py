from csv import DictReader
from datetime import datetime
from typing import Dict
from django.core.management import BaseCommand

from licenses.models import Action, District, Status, Recipient
from pytz import UTC


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("Loading Actions...")
        for row in DictReader(open('./data/seed/actions.csv')):
            action = Action()
            print(row)
            action.code = row['code']
            action.description = row['description']
            action.save()
        print("\n")

        print("Loading Districts...")
        for row in DictReader(open('./data/seed/districts.csv')):
            district = District()
            district.code = row['code']
            district.description = row['description']
            district.save()
        print("\n")

        print("Loading Recipients...")
        for row in DictReader(open('./data/seed/recipients.csv')):
            recipient = Recipient()
            recipient.email_address = row['email_address']
            recipient.first_name = row['first_name']
            recipient.last_name = row['last_name']
            recipient.save()
        print("\n")

        print("Loading Statuses...")
        for row in DictReader(open('./data/seed/statuses.csv')):
            status = Status()
            status.code = row['code']
            status.description = row['description']
            status.save()
        print("\n")
