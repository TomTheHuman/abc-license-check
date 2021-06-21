from os import error
import db
import csv
import mysql.connector
from mysql.connector import Error
import datetime
from django.core.management import BaseCommand

from licenses.models import StatusChange, NewApplication, IssuedLicense

class Command(BaseCommand):

    def handle(self, *args, **options):

        # Collect data from reports
        self.collect_status_changes()
        # data_issued_licenses = collect_issued_licenses()
        # data_new_applications = collect_new_applications()

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
                    status_change = StatusChange()
                    status_change.lic_num = int(row[0].strip())
                    status_change.status_from = row[1][:(row[1].find(' '))].strip()
                    status_change.status_to = row[1][(row[1].find(' ') + 1):].strip()
                    status_change.lic_type = int(row[2][:(row[2].find(' '))].strip())
                    status_change.lic_dup = int(row[2][(row[2].find('|') + 1):].strip()) 
                    
                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set
                    datetime_issue = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' and len(row[3]) > 0 else ''
                    status_change.issue_date = datetime_issue.strftime('%Y-%m-%d') if datetime_issue != '' else None

                    # Strips datetime string from report and formats using format_str definition above (if column string not empty)
                    # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set
                    datetime_exp = datetime.datetime.strptime(row[4].strip(), format_str) if row[4].strip() != '' and len(row[4]) > 0 else ''
                    status_change.exp_date = datetime_exp.strftime('%Y-%m-%d') if datetime_exp != '' else None
                    
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
                            status_change.acct_street = None
                            status_change.acct_city = None
                            status_change.acct_state = None
                            status_change.acct_zip = None
                    else:
                        status_change.acct_name = None
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
                        else:
                            status_change.acct_street = None
                            status_change.acct_city = None
                            status_change.acct_state = None
                            status_change.acct_zip = None
                        
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
                        status_change.mail_city = None
                        status_change.mail_state = None
                        status_change.mail_zip = None
                    else:
                        status_change.mail_street = None
                        status_change.mail_city = None
                        status_change.mail_state = None
                        status_change.mail_zip = None

                    # Local list variable created to store separated values from Trans From / To
                    # Both values separated by forward slash
                    # This column sometimes contains no values, a from value, or a from and to value
                    # Logic handles the above cases and sets omitted values to None where applicable
                    trans_from_to = row[7].split('/ ')
                    if len(trans_from_to) == 0:
                        status_change.trans_from = None
                        status_change.trans_to = None
                    elif len(trans_from_to) == 1:
                        status_change.trans_from = trans_from_to[0].strip()
                        status_change.trans_to = None
                    elif len(trans_from_to) == 2:
                        status_change.trans_from = trans_from_to[0].strip()
                        status_change.trans_to = trans_from_to[1].strip()

                    # If the column below is not an empty string, it is stored as dict value
                    # If string is empty, value is set to None
                    status_change.geocode = int(row[11]) if len(row[11]) > 0 else None

                status_change.save()

        except IOError:
            print('There was a problem opening report_status_changes.csv. The file may not exist in the data directory.')

    # def collect_issued_licenses():
    #     '''
    #     Tries to open report_issued_licenses.csv file from data directory
    #     Creates list to store dictionaries for each row of data
    #     Creates dictionaries used to collect formatted data from the report columns
    #     Strips, slices, and formats data from report to match MySQL data definitions

    #     Returns data_issued_licenses (list of dictionaries referenced above)

    #     If file does not exist, IOError exception is thrown - error message printed
    #     '''
    #     try:
    #         with open('./data/report_issued_licenses.csv') as datafile:
    #             # Initialize list to store row dicts
    #             data_issued_licenses = []

    #             data_reader = csv.reader(datafile)
    #             next(data_reader)

    #             # String format used in ABC reports            
    #             format_str = '%m/%d/%Y'
    #             for row in data_reader:
    #                 # Initialize new dict to store row data
    #                 item = {}
    #                 item['lic_num'] = int(row[0].strip())
    #                 item['status'] = row[1].strip()
    #                 item['lic_type'] = int(row[2][:(row[2].find(' '))].strip())
    #                 item['lic_dup'] = int(row[2][(row[2].find('|') + 1):].strip())
                    
    #                 # Strips datetime string from report and formats using format_str definition above (if column string not empty)
    #                 # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set               
    #                 datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' and len(row[3]) > 0 else ''
    #                 item['exp_date'] = datetime_exp.strftime('%Y-%m-%d') if datetime_exp != '' else None

    #                 # Local list variable created to store delimitted values from Primary Owner and Premises Addr. report column
    #                 # This column will sometimes include the account name (with "DBA: " prefix)
    #                 # This column will sometimes include the account premises address (if no address, the comma-separator between street and city will remain)
    #                 # Logic handles all of the above cases and sets omitted values to None where applcable
    #                 prim_own_addr = row[4].split('                            ')
    #                 if(prim_own_addr[0][:3] == 'DBA'):
    #                     item['acct_name'] = prim_own_addr[0][5:].strip()
    #                     item['acct_own'] = prim_own_addr[1].strip()

    #                     # If the primary address has been omitted, the report leaves the comma-separator for street and city
    #                     # This logic will check if there is a single comma (no address info) before continuing
    #                     if prim_own_addr[2].strip() != ',':
    #                         item['acct_street'] = prim_own_addr[2][:-1].strip()

    #                         acct_cityStateZip = prim_own_addr[3]
    #                         item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

    #                         acct_stateZip = acct_cityStateZip.split(', ')[1]
    #                         item['acct_state'] = acct_stateZip[:2].strip()
    #                         item['acct_zip'] = acct_stateZip[4:].strip()
    #                     else:
    #                         item['acct_street'] = None
    #                         item['acct_city'] = None
    #                         item['acct_state'] = None
    #                         item['acct_zip'] = None
    #                 else:
    #                     item['acct_name'] = None
    #                     item['acct_own'] = prim_own_addr[0].strip()
                        
    #                     # If the primary address has been omitted, the report leaves the comma-separator for street and city
    #                     # This logic will check if there is a single comma (no address info) before continuing
    #                     if prim_own_addr[1].strip() != ',':
    #                         item['acct_street'] = prim_own_addr[1][:-1].strip()

    #                         acct_cityStateZip = prim_own_addr[2]
    #                         item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

    #                         acct_stateZip = acct_cityStateZip.split(', ')[1]
    #                         item['acct_state'] = acct_stateZip[:2].strip()
    #                         item['acct_zip'] = acct_stateZip[4:].strip()
    #                     else:
    #                         item['acct_street'] = None
    #                         item['acct_city'] = None
    #                         item['acct_state'] = None
    #                         item['acct_zip'] = None

    #                 # Local list variable created to store delimitted values from Mailing Addr. report column
    #                 # This column will either contain the full address string or an empty string
    #                 # Logic handles the above cases and sets omitted values to None where applicable
    #                 mail_addr = row[5].split('                              ')
    #                 if len(mail_addr) > 1:
    #                     item['mail_street'] = mail_addr[0].strip()

    #                     mail_city_state_zip = mail_addr[1]
    #                     item['mail_city'] = mail_city_state_zip.split(', ')[0].strip()

    #                     mail_state_zip = mail_city_state_zip.split(', ')[1]
    #                     item['mail_state'] = mail_state_zip[:2].strip()
    #                     item['mail_zip'] = mail_state_zip[4:].strip()
    #                 elif len(mail_addr) > 0:
    #                     item['mail_street'] = mail_addr[0].strip()
    #                     item['mail_city'] = None
    #                     item['mail_state'] = None
    #                     item['mail_zip'] = None
    #                 else:
    #                     item['mail_street'] = None
    #                     item['mail_city'] = None
    #                     item['mail_state'] = None
    #                     item['mail_zip'] = None

    #                 # If each of the columns below are not empty strings, they are stored as dict values
    #                 # If strings are empty, values are set to None
    #                 item['action'] = row[6] if len(row[6]) > 0 else None
    #                 item['conditions'] = row[7] if len(row[7]) > 0 else None
    #                 item['escrow_addr'] = row[8] if len(row[8]) > 0 else None
    #                 item['district_code'] = int(row[9]) if len(row[9]) > 0 else None
    #                 item['geocode'] = int(row[10]) if len(row[10]) > 0 else None

    #                 data_issued_licenses.append(item)

    #             return data_issued_licenses
    #     except IOError:
    #         print('There was a problem opening report_issued_licenses.csv. The file may not exist in the data directory.')

    # def collect_new_applications():
    #     '''
    #     Tries to open report_new_applications.csv file from data directory
    #     Creates list to store dictionaries for each row of data
    #     Creates dictionaries used to collect formatted data from the report columns
    #     Strips, slices, and formats data from report to match MySQL data definitions

    #     Returns data_new_applications (list of dictionaries referenced above)

    #     If file does not exist, IOError exception is thrown - error message printed
    #     '''
    #     try:
    #         with open('./data/report_new_applications.csv') as datafile:
    #             # Initialize list to store row dicts
    #             data_new_applications = []

    #             data_reader = csv.reader(datafile)
    #             next(data_reader)

    #             # String format used in ABC reports
    #             format_str = '%m/%d/%Y'
    #             for row in data_reader:
    #                 # Initialize new dict to store row data
    #                 item = {}
    #                 item['lic_num'] = int(row[0].strip())
    #                 item['status'] = row[1].strip()
    #                 item['lic_type'] = int(row[2][:(row[2].find(' '))].strip())
    #                 item['lic_dup'] = int(row[2][(row[2].find('|') + 1):].strip())

    #                 # Strips datetime string from report and formats using format_str definition above (if column string not empty)
    #                 # If the above step resulted in a value (not empty string) datetime is converted to MySQL date format, otherwise None value set
    #                 datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[4].strip() != '' and len(row[3]) > 0 else ''
    #                 item['exp_date'] = datetime_exp.strftime('%Y-%m-%d') if datetime_exp != '' else None

    #                 # Local list variable created to store delimitted values from Primary Owner and Premises Addr. report column
    #                 # This column will sometimes include the account name (with "DBA: " prefix)
    #                 # This column will sometimes include the account premises address (if no address, the comma-separator between street and city will remain)
    #                 # Logic handles all of the above cases and sets omitted values to None where applcable
    #                 prim_own_addr = row[4].split('                        ')
    #                 if(prim_own_addr[0][:3] == 'DBA'):
    #                     item['acct_name'] = prim_own_addr[0][5:].strip()
    #                     item['acct_own'] = prim_own_addr[1].strip()

    #                     # If the primary address has been omitted, the report leaves the comma-separator for street and city
    #                     # This logic will check if there is a single comma (no address info) before continuing
    #                     if prim_own_addr[2].strip() != ',':
    #                         item['acct_street'] = prim_own_addr[2][:-1].strip()

    #                         acct_cityStateZip = prim_own_addr[3]
    #                         item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

    #                         acct_stateZip = acct_cityStateZip.split(', ')[1]
    #                         item['acct_state'] = acct_stateZip[:2].strip()
    #                         item['acct_zip'] = acct_stateZip[4:].strip()
    #                     else:
    #                         item['acct_street'] = None
    #                         item['acct_city'] = None
    #                         item['acct_state'] = None
    #                         item['acct_zip'] = None
    #                 else:
    #                     item['acct_name'] = None
    #                     item['acct_own'] = prim_own_addr[0].strip()
                        
    #                     # If the primary address has been omitted, the report leaves the comma-separator for street and city
    #                     # This logic will check if there is a single comma (no address info) before continuing
    #                     if prim_own_addr[1].strip() != ',':
    #                         item['acct_street'] = prim_own_addr[1][:-1].strip()

    #                         acct_cityStateZip = prim_own_addr[2]
    #                         item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

    #                         acct_stateZip = acct_cityStateZip.split(', ')[1]
    #                         item['acct_state'] = acct_stateZip[:2].strip()
    #                         item['acct_zip'] = acct_stateZip[4:].strip()
    #                     else:
    #                         item['acct_street'] = None
    #                         item['acct_city'] = None
    #                         item['acct_state'] = None
    #                         item['acct_zip'] = None

    #                 # Local list variable created to store delimitted values from Mailing Addr. report column
    #                 # This column will either contain the full address string or an empty string
    #                 # Logic handles the above cases and sets omitted values to None where applicable
    #                 mail_addr = row[5].split('                              ')
    #                 if len(mail_addr) > 1:
    #                     item['mail_street'] = mail_addr[0].strip()

    #                     mail_cityStateZip = mail_addr[1]
    #                     item['mail_city'] = mail_cityStateZip.split(', ')[0].strip()

    #                     mail_stateZip = mail_cityStateZip.split(', ')[1]
    #                     item['mail_state'] = mail_stateZip[:2].strip()
    #                     item['mail_zip'] = mail_stateZip[4:].strip()
    #                 elif len(mail_addr) > 0:
    #                     item['mail_street'] = mail_addr[0].strip()
    #                     item['mail_city'] = None
    #                     item['mail_state'] = None
    #                     item['mail_zip'] = None
    #                 else:
    #                     item['mail_street'] = None
    #                     item['mail_city'] = None
    #                     item['mail_state'] = None
    #                     item['mail_zip'] = None

    #                 # If each of the columns below are not empty strings, they are stored as dict values
    #                 # If strings are empty, values are set to None
    #                 item['action'] = row[6] if len(row[6]) > 0 else None
    #                 item['conditions'] = row[7] if len(row[7]) > 0 else None
    #                 item['escrow_addr'] = row[8] if len(row[8]) > 0 else None
    #                 item['district_code'] = int(row[9]) if len(row[9]) > 0 else None
    #                 item['geocode'] = int(row[10]) if len(row[10]) > 0 else None

    #                 data_new_applications.append(item)
                
    #             return data_new_applications
    #     except IOError:
    #         print('There was a problem opening report_new_applications.csv. The file may not exist in the data directory.')


    # # TODO Create dynamic query that lists colums to insert by using dict keys (must be named the same as table columns)
    # def upload_status_changes(data):
    #     '''
    #     Takes data list containing stripped information from rows in report
    #     Queries MySQL database to insert data into status_changes table
    #     Returns nothing
    #     '''
    #     print('Uploading to status_changes...')

    #     # Creates database connection
    #     conn = db.get_db()

    #     # Creates dynamic query string with variable strings as values
    #     query = f'''INSERT INTO status_changes (
    #         lic_num,
    #         status_from,
    #         status_to,
    #         lic_type,
    #         lic_dup,
    #         issue_date,
    #         exp_date,
    #         acct_name,
    #         acct_owner,
    #         acct_street,
    #         acct_city,
    #         acct_state,
    #         acct_zip,
    #         mail_street,
    #         mail_city,
    #         mail_state,
    #         mail_zip,
    #         trans_from,
    #         trans_to,
    #         geocode
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    #     for item in data:

    #         try:
    #             cursor = conn.cursor()

    #             # Sets arguments list to list of values in data list
    #             # Keys have to be in same order as columns listed in query above for values to properly align
    #             args = list(item.values())
    #             cursor.execute(query, args)

    #             if cursor.lastrowid:
    #                 print('Last Insert ID: ', cursor.lastrowid)
    #             else:
    #                 print('Last Insert ID Not Found!')
                
    #             conn.commit()
            
    #         except Error as e:
    #             print(e)
        
    #     print('Upload complete!')

    #     conn.close()

    # def upload_issued_licenses(data):
    #     '''
    #     Takes data list containing stripped information from rows in report
    #     Queries MySQL database to insert data into issued_licenses table
    #     Returns nothing
    #     '''
    #     print('Uploading to issued_licenses...')

    #     # Creates database connection
    #     conn = db.get_db()

    #     # Creates dynamic query string with variable strings as values
    #     query = f'''INSERT INTO issued_licenses(
    #         lic_num,
    #         status,
    #         lic_type,
    #         lic_dup,
    #         exp_date,
    #         acct_name,
    #         acct_own,
    #         acct_street,
    #         acct_city,
    #         acct_state,
    #         acct_zip,
    #         mail_street,
    #         mail_city,
    #         mail_state,
    #         mail_zip,
    #         action,
    #         conditions,
    #         escrow,
    #         district_code,
    #         geocode
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    #     for item in data:

    #         try:
    #             cursor = conn.cursor()

    #             # Sets arguments list to list of values in data list
    #             # Keys have to be in same order as columns listed in query above for values to properly align
    #             args = list(item.values())
    #             cursor.execute(query, args)

    #             if cursor.lastrowid:
    #                 print('Last Insert ID: ', cursor.lastrowid)
    #             else:
    #                 print('Last Insert ID Not Found!')

    #             conn.commit()
            
    #         except Error as e:
    #             print(e)
        
    #     print('Upload complete!')

    #     conn.close()

    # def upload_new_applications(data):
    #     '''
    #     Takes data list containing stripped information from rows in report
    #     Queries MySQL database to insert data into new_applications table
    #     Returns nothing
    #     '''
    #     print('Uploading to new_applications...')    
        
    #     # Creates database connection
    #     conn = db.get_db()

    #     # Creates dynamic query string with variable strings as values
    #     query = f'''INSERT INTO issued_licenses(
    #         lic_num,
    #         status,
    #         lic_type,
    #         lic_dup,
    #         exp_date,
    #         acct_name,
    #         acct_own,
    #         acct_street,
    #         acct_city,
    #         acct_state,
    #         acct_zip,
    #         mail_street,
    #         mail_city,
    #         mail_state,
    #         mail_zip,
    #         action,
    #         conditions,
    #         escrow,
    #         district_code,
    #         geocode
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    #     for item in data:

    #         try:
    #             cursor = conn.cursor()

    #             # Sets arguments list to list of values in data list
    #             # Keys have to be in same order as columns listed in query above for values to properly align
    #             args = list(item.values())
    #             cursor.execute(query, args)

    #             if cursor.lastrowid:
    #                 print('Last Insert ID: ', cursor.lastrowid)
    #             else:
    #                 print('Last Insert ID Not Found!')

    #             conn.commit()
            
    #         except Error as e:
    #             print(e)
        
    #     print('Upload complete!')

    #     conn.close()
    

