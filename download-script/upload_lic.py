import db
import csv
import mysql.connector
from mysql.connector import Error
import datetime

def collect_status_changes():
    with open('./data/report_status_changes.csv') as datafile:
        data_status_changes = []
        data_reader = csv.reader(datafile)
        next(data_reader)
        format_str = '%m/%d/%Y'
        for row in data_reader:
            item = {}
            item['lic_number'] = row[0].strip()
            item['status_from'] = row[1][:(row[1].find(' '))].strip()
            item['status_to'] = row[1][(row[1].find(' ') + 1):].strip()
            item['lic_type'] = row[2][:(row[2].find(' ') - 2)].strip()
            item['lic_dup'] = row[2][-2:]

            if len(row[3]) > 0:
                datetime_issue = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' else None
                item['issue_date'] = datetime_issue

            if len(row[4]) > 0:
                datetime_exp = datetime.datetime.strptime(row[4].strip(), format_str) if row[4].strip() != '' else None
                item['exp_date'] = datetime_exp
            
            prim_own_addr = row[5].split('                        ')
            if(prim_own_addr[0][:3] == 'DBA'):
                item['acct_name'] = prim_own_addr[0][5:].strip()
                item['acct_own'] = prim_own_addr[1].strip()
                item['acct_street'] = prim_own_addr[2][:-1].strip()

                acct_cityStateZip = prim_own_addr[3]
                item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

                acct_stateZip = acct_cityStateZip.split(', ')[1]
                item['acct_state'] = acct_stateZip[:2].strip()
                item['acct_zip'] = acct_stateZip[4:].strip()
            else:
                item['acct_name'] = ''
                item['acct_own'] = prim_own_addr[0].strip()
                item['acct_street'] = prim_own_addr[1][:-1].strip()
                
                acct_cityStateZip = prim_own_addr[2]
                item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

                acct_stateZip = acct_cityStateZip.split(', ')[1]
                item['acct_state'] = acct_stateZip[:2].strip()
                item['acct_zip'] = acct_stateZip[4:].strip()

            mail_addr = row[6].split('                              ')
            if len(mail_addr) > 1:
                item['mail_street'] = mail_addr[0].strip()

                mail_cityStateZip = mail_addr[1]
                item['mail_city'] = mail_cityStateZip.split(', ')[0].strip()

                mail_stateZip = mail_cityStateZip.split(', ')[1]
                item['mail_state'] = mail_stateZip[:2].strip()
                item['mail_zip'] = mail_stateZip[4:].strip()
            elif len(mail_addr) > 0:
                item['mail_street'] = mail_addr[0].strip()
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''
            else:
                item['mail_street'] = ''
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''

            trans_from_to = row[7].split('/ ')
            if len(trans_from_to) == 0:
                item['trans_from'] = ""
                item['trans_to'] = ""
            elif len(trans_from_to) == 1:
                item['trans_from'] = trans_from_to[0].strip()
                item['trans_to'] = ""
            elif len(trans_from_to) == 2:
                item['trans_from'] = trans_from_to[0].strip()
                item['trans_to'] = trans_from_to[1].strip()

            item['geo_code'] = row[11] if len(row[11]) > 0 else None
            data_status_changes.append(item)

        return data_status_changes

def collect_issued_licenses():
    with open('./data/report_issued_licenses.csv') as datafile:
        data_issued_licenses = []
        data_reader = csv.reader(datafile)
        next(data_reader)
        format_str = '%m/%d/%Y'
        for row in data_reader:
            item = {}
            item['lic_number'] = row[0].strip()
            item['status'] = row[1].strip()
            item['lic_type'] = row[2].strip()
            
            if len(row[3]) > 0:
                datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' else None
                item['exp_date'] = datetime_exp
            
            prim_own_addr = row[4].split('                            ')
            if(prim_own_addr[0][:3] == 'DBA'):
                item['acct_name'] = prim_own_addr[0][5:].strip()
                item['acct_own'] = prim_own_addr[1].strip()
                item['acct_street'] = prim_own_addr[2][:-1].strip()

                acct_city_state_zip = prim_own_addr[3]
                item['acct_city'] = acct_city_state_zip.split(', ')[0].strip()

                acct_state_zip = acct_city_state_zip.split(', ')[1]
                item['acct_state'] = acct_state_zip[:2].strip()
                item['acct_zip'] = acct_state_zip[4:].strip()
            else:
                item['acct_name'] = ''
                item['acct_own'] = prim_own_addr[0].strip()
                item['acct_street'] = prim_own_addr[1][:-1].strip()
                
                acct_city_state_zip = prim_own_addr[2]
                item['acct_city'] = acct_city_state_zip.split(', ')[0].strip()

                acct_state_zip = acct_city_state_zip.split(', ')[1]
                item['acct_state'] = acct_state_zip[:2].strip()
                item['acct_zip'] = acct_state_zip[4:].strip()

            mail_addr = row[5].split('                              ')
            if len(mail_addr) > 1:
                item['mail_street'] = mail_addr[0].strip()

                mail_city_state_zip = mail_addr[1]
                item['mail_city'] = mail_city_state_zip.split(', ')[0].strip()

                mail_state_zip = mail_city_state_zip.split(', ')[1]
                item['mail_state'] = mail_state_zip[:2].strip()
                item['mail_zip'] = mail_state_zip[4:].strip()
            elif len(mail_addr) > 0:
                item['mail_street'] = mail_addr[0].strip()
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''
            else:
                item['mail_street'] = ''
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''

            item['action'] = row[6] if len(row[6]) > 0 else None
            item['conditions'] = row[7] if len(row[7]) > 0 else None
            item['escrow_addr'] = row[8] if len(row[8]) > 0 else None
            item['district_code'] = row[9] if len(row[9]) > 0 else None
            item['geo_code'] = row[10] if len(row[10]) > 0 else None

            data_issued_licenses.append(item)

        return data_issued_licenses

def collect_new_applications():
    with open('./data/report_new_applications.csv') as datafile:
        data_new_applications = []
        data_reader = csv.reader(datafile)
        next(data_reader)
        format_str = '%m/%d/%Y'
        for row in data_reader:
            item = {}
            item['lic_number'] = row[0].strip()
            item['status'] = row[1].strip()
            item['lic_type'] = row[2][:(row[2].find(' ') - 2)].strip()
            item['lic_dup'] = row[2][-2:]

            if len(row[3]) > 0:
                datetime_exp = datetime.datetime.strptime(row[3].strip(), format_str) if row[4].strip() != '' else None
                item['exp_date'] = datetime_exp
            
            prim_own_addr = row[4].split('                        ')
            if(prim_own_addr[0][:3] == 'DBA'):
                item['acct_name'] = prim_own_addr[0][5:].strip()
                item['acct_own'] = prim_own_addr[1].strip()
                item['acct_street'] = prim_own_addr[2][:-1].strip()

                acct_cityStateZip = prim_own_addr[3]
                item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

                acct_stateZip = acct_cityStateZip.split(', ')[1]
                item['acct_state'] = acct_stateZip[:2].strip()
                item['acct_zip'] = acct_stateZip[4:].strip()
            else:
                item['acct_name'] = ''
                item['acct_own'] = prim_own_addr[0].strip()
                item['acct_street'] = prim_own_addr[1][:-1].strip()
                
                acct_cityStateZip = prim_own_addr[2]
                item['acct_city'] = acct_cityStateZip.split(', ')[0].strip()

                acct_stateZip = acct_cityStateZip.split(', ')[1]
                item['acct_state'] = acct_stateZip[:2].strip()
                item['acct_zip'] = acct_stateZip[4:].strip()

            mail_addr = row[5].split('                              ')
            if len(mail_addr) > 1:
                item['mail_street'] = mail_addr[0].strip()

                mail_cityStateZip = mail_addr[1]
                item['mail_city'] = mail_cityStateZip.split(', ')[0].strip()

                mail_stateZip = mail_cityStateZip.split(', ')[1]
                item['mail_state'] = mail_stateZip[:2].strip()
                item['mail_zip'] = mail_stateZip[4:].strip()
            elif len(mail_addr) > 0:
                item['mail_street'] = mail_addr[0].strip()
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''
            else:
                item['mail_street'] = ''
                item['mail_city'] = ''
                item['mail_state'] = ''
                item['mail_zip'] = ''


            item['action'] = row[6] if len(row[6]) > 0 else None
            item['conditions'] = row[7] if len(row[7]) > 0 else None
            item['escrow_addr'] = row[8] if len(row[8]) > 0 else None
            item['district_code'] = row[9] if len(row[9]) > 0 else None
            item['geo_code'] = row[10] if len(row[10]) > 0 else None

            data_new_applications.append(item)
        
        return data_new_applications

def upload_status_changes(data):
    conn = db.get_db()
    query = f'''INSERT INTO status_changes(
        lic_num,
        status_from,
        status_to,
        lic_type,
        lic_dup,
        issue_date,
        exp_date,
        acct_name,
        acct_owner,
        acct_street,
        acct_city,
        acct_state,
        acct_zip,
        mail_street,
        mail_city,
        mail_state,
        mail_zip,
        trans_from,
        trans_to,
        geo_code
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    for item in data:

        try:
            cursor = conn.cursor()
            for key in item.keys():
                print(key, ": ", item[key])
            cursor.execute(query, item.values())

            if cursor.lastrowid:
                print('Last Insert ID: ', cursor.lastrowid)
            else:
                print('Last Insert ID Not Found!')

            conn.commit()
        
        except Error as e:
            print(e)
    
    print('Upload complete!')

    conn.close()

def upload_issued_licenses(data):
    conn = db.get_db()
    query = f'''INSERT INTO issued_licenses(
        lic_num,
        status,
        lic_type,
        lic_dup,
        exp_date,
        acct_name,
        acct_own,
        acct_street,
        acct_city,
        acct_state,
        acct_zip,
        mail_street,
        mail_city,
        mail_state,
        mail_zip,
        action,
        conditions,
        escrow,
        district_code,
        geo_code
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    for item in data:

        try:
            cursor = conn.cursor()
            for key in item.keys():
                print(key, ": ", item[key])
            cursor.execute(query, item.values())

            if cursor.lastrowid:
                print('Last Insert ID: ', cursor.lastrowid)
            else:
                print('Last Insert ID Not Found!')

            conn.commit()
        
        except Error as e:
            print(e)
    
    print('Upload complete!')

    conn.close()

def upload_new_applications(data):
    conn = db.get_db()
    query = f'''INSERT INTO issued_licenses(
        lic_num,
        status,
        lic_type,
        lic_dup,
        exp_date,
        acct_name,
        acct_own,
        acct_street,
        acct_city,
        acct_state,
        acct_zip,
        mail_street,
        mail_city,
        mail_state,
        mail_zip,
        action,
        conditions,
        escrow,
        district_code,
        geo_code
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    for item in data:

        try:
            cursor = conn.cursor()
            for key in item.keys():
                print(key, ": ", item[key])
            cursor.execute(query, item.values())

            if cursor.lastrowid:
                print('Last Insert ID: ', cursor.lastrowid)
            else:
                print('Last Insert ID Not Found!')

            conn.commit()
        
        except Error as e:
            print(e)
    
    print('Upload complete!')

    conn.close()
 
if __name__ == "__main__":

    # Collect data from reports
    # TODO Check to make sure file exists first / handle open errors
    data_status_changes = collect_status_changes()
    data_issued_licenses = collect_issued_licenses()
    data_new_applications = collect_new_applications()

    # Upload data from files to MySQL
    upload_status_changes(data_status_changes)
    upload_issued_licenses(data_issued_licenses)
    upload_new_applications(data_new_applications)