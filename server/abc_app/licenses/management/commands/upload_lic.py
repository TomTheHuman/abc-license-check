from os import error
# import db
import csv
# import mysql.connector
# from mysql.connector import Error
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.management import BaseCommand

from licenses.models import Report, Action, District, Status

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Collect data from reports
        self.collect_status_changes()
        self.collect_issued_licenses()
        self.collect_new_applications()

        # # Upload data from files to MySQL
        # upload_status_changes(data_status_changes)
        # upload_issued_licenses(data_issued_licenses)
        # upload_new_applications(data_new_applications)

    def collect_status_changes(self):
        '''
        Tries to open report_status_changes.csv file from data directory
        Creates list to store dictionaries for each row of data
        Creates dictionaries used to collect formatted data from the report columns
        Strips, slices, and formats data from report to match MySQL data definitions

        Returns data_status_changes (list of dictionaries referenced above)

        If file does not exist, IOError exception is thrown - error message printed
        '''
        try:
            with open('./data/report_status_changes.csv') as datafile:
                # Initialize list to store row dicts
                data_status_changes = []

                data_reader = csv.reader(datafile)
                next(data_reader)

                # String format used in ABC reports
                format_str = '%m/%d/%Y'
                for row in data_reader:
                    # Initialize new dict to store row data
                    status_change = Report()
                    status_change.report_type = "status_change"
                    status_change.lic_num = int(row[0].strip())

                    status_code = row[1][:(row[1].find(' '))].strip()
                    status_from = Status.objects.get(code=status_code)
                    status_change.status_from = status_from

                    status_code = row[1][(row[1].find(' ') + 1):].strip()
                    status_to = Status.objects.get(code=status_code)
                    status_change.status_to = status_to

                    status_change.lic_type = int(row[2][:(row[2].find(' '))].strip())
                    status_change.lic_dup = int(row[2][(row[2].find('|') + 1):].strip()) 
                    
                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set

                    datetime_issue = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' and len(row[3]) > 0 else ''
                    status_change.issue_date = datetime_issue.strftime('%Y-%m-%d %H:%M:%S') if datetime_issue != '' else None

                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set
                    datetime_exp = datetime.datetime.strptime(row[4].strip(), format_str) if row[4].strip() != '' and len(row[4]) > 0 else ''
                    status_change.exp_date = datetime_exp.strftime('%Y-%m-%d %H:%M:%S') if datetime_exp != '' else None
                    
                    # Local list variable created to store delimitted values from Primary Owner and Premises Addr. report column
                    # This column will sometimes include the account name (with "DBA: " prefix)
                    # This column will sometimes include the account premises address (if no address, the comma-separator between street and city will remain)
                    # Logic handles all of the above cases and sets omitted values to None where applcable
                    prim_own_addr = row[5].split('                        ')
                    if(prim_own_addr[0][:3] == 'DBA'):
                        status_change.acct_name = prim_own_addr[0][5:].strip()
                        status_change.acct_own = prim_own_addr[1].strip()

                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[2].strip() != ',':
                            status_change.acct_street = prim_own_addr[2][:-1].strip()

                            acct_cityStateZip = prim_own_addr[3]
                            status_change.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            status_change.acct_state = acct_stateZip[:2].strip()
                            status_change.acct_zip = acct_stateZip[4:].strip()
                    else:
                        status_change.acct_own = prim_own_addr[0].strip()
                        
                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[1].strip() != ',':
                            status_change.acct_street = prim_own_addr[1][:-1].strip()

                            acct_cityStateZip = prim_own_addr[2]
                            status_change.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            status_change.acct_state = acct_stateZip[:2].strip()
                            status_change.acct_zip = acct_stateZip[4:].strip()
                        
                    # Local list variable created to store delimitted values from Mailing Addr. report column
                    # This column will either contain the full address string or an empty string
                    # Logic handles the above cases and sets omitted values to None where applicable
                    mail_addr = row[6].split('                              ')
                    if len(mail_addr) > 1:
                        status_change.mail_street = mail_addr[0].strip()

                        mail_cityStateZip = mail_addr[1]
                        status_change.mail_city = mail_cityStateZip.split(', ')[0].strip()

                        mail_stateZip = mail_cityStateZip.split(', ')[1]
                        status_change.mail_state = mail_stateZip[:2].strip()
                        status_change.mail_zip = mail_stateZip[4:].strip()
                    elif len(mail_addr) > 0 and not mail_addr[0] == None:
                        status_change.mail_street = mail_addr[0].strip()

                    # Local list variable created to store separated values from Trans From / To
                    # Both values separated by forward slash
                    # This column sometimes contains no values, a from value, or a from and to value
                    # Logic handles the above cases and sets omitted values to None where applicable
                    trans_from_to = row[7].split('/ ')
                    if len(trans_from_to) == 1 and len(trans_from_to[0]) > 0:
                        status_change.trans_from = trans_from_to[0].strip()
                        status_change.trans_to = None
                    elif len(trans_from_to) == 2:
                        status_change.trans_from = trans_from_to[0].strip()
                        status_change.trans_to = trans_from_to[1].strip()

                    code = int(row[10].strip())
                    district = District.objects.get(code=code)
                    status_change.district = district

                    # If the column below is not an empty string, it is stored as dict value
                    # If string is empty, value is set to None
                    status_change.geocode = int(row[11]) if len(row[11]) > 0 else None

                    status_change.save()


        except IOError:
            print('There was a problem opening report_status_changes.csv. The file may not exist in the data directory.')

    def collect_issued_licenses(self):
        '''
        Tries to open report_issued_licenses.csv file from data directory
        Creates list to store dictionaries for each row of data
        Creates dictionaries used to collect formatted data from the report columns
        Strips, slices, and formats data from report to match MySQL data definitions

        Returns data_issued_licenses (list of dictionaries referenced above)

        If file does not exist, IOError exception is thrown - error message printed
        '''
        try:
            with open('./data/report_issued_licenses.csv') as datafile:
                data_reader = csv.reader(datafile)
                next(data_reader)

                # String format used in ABC reports            
                format_str = '%m/%d/%Y'
                for row in data_reader:
                    # Initialize new dict to store row data
                    issued_license = Report()
                    issued_license.report_type = "issued_license"
                    issued_license.lic_num = int(row[0].strip())

                    # Issued Licenses use the status description instead of code
                    status_desc = row[1].strip()
                    status = Status.objects.get(description=status_desc)
                    issued_license.status = status

                    issued_license.lic_type = int(row[2][:(row[2].find(' '))].strip())
                    issued_license.lic_dup = int(row[2][(row[2].find('|') + 1):].strip())
                    
                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set               
                    datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' and len(row[3]) > 0 else ''
                    issued_license.exp_date = datetime_exp.strftime('%Y-%m-%d') if datetime_exp != '' else None

                    # Local list variable created to store delimitted values from Primary Owner and Premises Addr. report column
                    # This column will sometimes include the account name (with "DBA: " prefix)
                    # This column will sometimes include the account premises address (if no address, the comma-separator between street and city will remain)
                    # Logic handles all of the above cases and sets omitted values to None where applcable
                    prim_own_addr = row[4].split('                            ')
                    if(prim_own_addr[0][:3] == 'DBA'):
                        issued_license.acct_name = prim_own_addr[0][5:].strip()
                        issued_license.acct_own = prim_own_addr[1].strip()

                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[2].strip() != ',':
                            issued_license.acct_street = prim_own_addr[2][:-1].strip()

                            acct_cityStateZip = prim_own_addr[3]
                            issued_license.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            issued_license.acct_state = acct_stateZip[:2].strip()
                            issued_license.acct_zip = acct_stateZip[4:].strip()
                        else:
                            issued_license.acct_street = None
                            issued_license.acct_city = None
                            issued_license.acct_state = None
                            issued_license.acct_zip = None
                    else:
                        issued_license.acct_name = None
                        issued_license.acct_own = prim_own_addr[0].strip()
                        
                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[1].strip() != ',':
                            issued_license.acct_street = prim_own_addr[1][:-1].strip()

                            acct_cityStateZip = prim_own_addr[2]
                            issued_license.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            issued_license.acct_state = acct_stateZip[:2].strip()
                            issued_license.acct_zip = acct_stateZip[4:].strip()
                        else:
                            issued_license.acct_street = None
                            issued_license.acct_city = None
                            issued_license.acct_state = None
                            issued_license.acct_zip = None

                    # Local list variable created to store delimitted values from Mailing Addr. report column
                    # This column will either contain the full address string or an empty string
                    # Logic handles the above cases and sets omitted values to None where applicable
                    mail_addr = row[5].split('                              ')
                    if len(mail_addr) > 1:
                        issued_license.mail_street = mail_addr[0].strip()

                        mail_city_state_zip = mail_addr[1]
                        issued_license.mail_city = mail_city_state_zip.split(', ')[0].strip()

                        mail_state_zip = mail_city_state_zip.split(', ')[1]
                        issued_license.mail_state = mail_state_zip[:2].strip()
                        issued_license.mail_zip = mail_state_zip[4:].strip()
                    elif len(mail_addr) > 0:
                        issued_license.mail_street = mail_addr[0].strip()
                        issued_license.mail_city = None
                        issued_license.mail_state = None
                        issued_license.mail_zip = None
                    else:
                        issued_license.mail_street = None
                        issued_license.mail_city = None
                        issued_license.mail_state = None
                        issued_license.mail_zip = None

                    # If each of the columns below are not empty strings, they are stored as dict values
                    # If strings are empty, values are set to None

                    # Get item from Action model
                    if len(row[6]) > 0:
                        code = row[6].strip()
                        action = Action.objects.filter(code=code).first()
                        issued_license.action = action

                    issued_license.conditions = row[7] if len(row[7]) > 0 else None
                    issued_license.escrow_addr = row[8] if len(row[8]) > 0 else None

                    # Get item from District model
                    code = int(row[9]) if len(row[9]) > 0 else None
                    district = District.objects.get(code=code)
                    issued_license.district = district

                    issued_license.geocode = int(row[10]) if len(row[10]) > 0 else None
                    issued_license.save()

        except IOError:
            print('There was a problem opening report_issued_licenses.csv. The file may not exist in the data directory.')

    def collect_new_applications(self):
        '''
        Tries to open report_new_applications.csv file from data directory
        Creates list to store dictionaries for each row of data
        Creates dictionaries used to collect formatted data from the report columns
        Strips, slices, and formats data from report to match MySQL data definitions

        Returns data_new_applications (list of dictionaries referenced above)

        If file does not exist, IOError exception is thrown - error message printed
        '''
        try:
            with open('./data/report_new_applications.csv') as datafile:
                # Initialize list to store row dicts
                data_new_applications = []

                data_reader = csv.reader(datafile)
                next(data_reader)

                # String format used in ABC reports
                format_str = '%m/%d/%Y'
                for row in data_reader:
                    # Initialize new dict to store row data
                    new_application = Report()
                    new_application.report_type = "new_application"
                    new_application.lic_num = int(row[0].strip())

                    # Issued Licenses use the status description instead of code
                    status_code = row[1].strip()
                    status = Status.objects.get(code=status_code)
                    new_application.status = status

                    new_application.lic_type = int(row[2][:(row[2].find(' '))].strip())
                    new_application.lic_dup = int(row[2][(row[2].find('|') + 1):].strip())

                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set
                    datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[4].strip() != '' and len(row[3]) > 0 else ''
                    new_application.exp_date = datetime_exp.strftime('%Y-%m-%d') if datetime_exp != '' else None

                    # Local list variable created to store delimitted values from Primary Owner and Premises Addr. report column
                    # This column will sometimes include the account name (with "DBA: " prefix)
                    # This column will sometimes include the account premises address (if no address, the comma-separator between street and city will remain)
                    # Logic handles all of the above cases and sets omitted values to None where applcable
                    prim_own_addr = row[4].split('                        ')
                    if(prim_own_addr[0][:3] == 'DBA'):
                        new_application.acct_name = prim_own_addr[0][5:].strip()
                        new_application.acct_own = prim_own_addr[1].strip()

                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[2].strip() != ',':
                            new_application.acct_street = prim_own_addr[2][:-1].strip()

                            acct_cityStateZip = prim_own_addr[3]
                            new_application.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            new_application.acct_state = acct_stateZip[:2].strip()
                            new_application.acct_zip = acct_stateZip[4:].strip()
                        else:
                            new_application.acct_street = None
                            new_application.acct_city = None
                            new_application.acct_state = None
                            new_application.acct_zip = None
                    else:
                        new_application.acct_name = None
                        new_application.acct_own = prim_own_addr[0].strip()
                        
                        # If the primary address has been omitted, the report leaves the comma-separator for street and city
                        # This logic will check if there is a single comma (no address info) before continuing
                        if prim_own_addr[1].strip() != ',':
                            new_application.acct_street = prim_own_addr[1][:-1].strip()

                            acct_cityStateZip = prim_own_addr[2]
                            new_application.acct_city = acct_cityStateZip.split(', ')[0].strip()

                            acct_stateZip = acct_cityStateZip.split(', ')[1]
                            new_application.acct_state = acct_stateZip[:2].strip()
                            new_application.acct_zip = acct_stateZip[4:].strip()
                        else:
                            new_application.acct_street = None
                            new_application.acct_city = None
                            new_application.acct_state = None
                            new_application.acct_zip = None

                    # Local list variable created to store delimitted values from Mailing Addr. report column
                    # This column will either contain the full address string or an empty string
                    # Logic handles the above cases and sets omitted values to None where applicable
                    mail_addr = row[5].split('                              ')
                    if len(mail_addr) > 1:
                        new_application.mail_street = mail_addr[0].strip()

                        mail_cityStateZip = mail_addr[1]
                        new_application.mail_city = mail_cityStateZip.split(', ')[0].strip()

                        mail_stateZip = mail_cityStateZip.split(', ')[1]
                        new_application.mail_state = mail_stateZip[:2].strip()
                        new_application.mail_zip = mail_stateZip[4:].strip()
                    elif len(mail_addr) > 0:
                        new_application.mail_street = mail_addr[0].strip()
                        new_application.mail_city = None
                        new_application.mail_state = None
                        new_application.mail_zip = None
                    else:
                        new_application.mail_street = None
                        new_application.mail_city = None
                        new_application.mail_state = None
                        new_application.mail_zip = None

                    # If each of the columns below are not empty strings, they are stored as dict values
                    # If strings are empty, values are set to None

                    # Get item from Action model
                    if len(row[6]) > 0:
                        code = row[6].strip()
                        action = Action.objects.filter(code=code).first()
                        new_application.action = action

                    new_application.conditions = row[7] if len(row[7]) > 0 else None
                    new_application.escrow_addr = row[8] if len(row[8]) > 0 else None

                    # Get item from District model
                    code = int(row[9]) if len(row[9]) > 0 else None
                    district = District.objects.get(code=code)
                    new_application.district = district

                    new_application.geocode = int(row[10]) if len(row[10]) > 0 else None
                    new_application.save()
                
                return data_new_applications
        except IOError:
            print('There was a problem opening report_new_applications.csv. The file may not exist in the data directory.')
