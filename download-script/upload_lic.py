import db
import csv
import mysql.connector
from mysql.connector import Error
import datetime

with open('./data/report.csv') as datafile:
    data = []
    dataReader = csv.reader(datafile)
    next(dataReader)
    format_str = '%m/%d/%Y'
    for row in dataReader:
        item = {}
        item['licNumber'] = row[0].strip()
        item['statusFrom'] = row[1][:(row[1].find(' '))].strip()
        item['statusTo'] = row[1][(row[1].find(' ') + 1):].strip()
        item['licType'] = row[2][:(row[2].find(' ') - 2)].strip()

        datetime_issue = datetime.datetime.strptime(row[3].strip(), format_str) if row[3].strip() != '' else None
        item['issueDate'] = datetime_issue

        datetime_exp = datetime.datetime.strptime(row[4].strip(), format_str) if row[4].strip() != '' else None
        item['expDate'] = datetime_exp
        
        primOwnAddr = row[5].split('                        ')
        if(primOwnAddr[0][:3] == 'DBA'):
            item['acctName'] = primOwnAddr[0][5:].strip()
            item['acctOwn'] = primOwnAddr[1].strip()
            item['acctStreet'] = primOwnAddr[2][:-1].strip()

            acctCityStateZip = primOwnAddr[3]
            item['acctCity'] = acctCityStateZip.split(', ')[0].strip()

            acctStateZip = acctCityStateZip.split(', ')[1]
            item['acctState'] = acctStateZip[:2].strip()
            item['acctZip'] = acctStateZip[4:].strip()
        else:
            item['acctName'] = ''
            item['acctOwn'] = primOwnAddr[0].strip()
            item['acctStreet'] = primOwnAddr[1][:-1].strip()
            
            acctCityStateZip = primOwnAddr[2]
            item['acctCity'] = acctCityStateZip.split(', ')[0].strip()

            acctStateZip = acctCityStateZip.split(', ')[1]
            item['acctState'] = acctStateZip[:2].strip()
            item['acctZip'] = acctStateZip[4:].strip()

        mailAddr = row[6].split('                              ')
        if len(mailAddr) > 1:
            item['mailStreet'] = mailAddr[0].strip()

            mailCityStateZip = mailAddr[1]
            item['mailCity'] = mailCityStateZip.split(', ')[0].strip()

            mailStateZip = mailCityStateZip.split(', ')[1]
            item['mailState'] = mailStateZip[:2].strip()
            item['mailZip'] = mailStateZip[4:].strip()
        elif len(mailAddr) > 0:
            item['mailStreet'] = mailAddr[0].strip()
            item['mailCity'] = ''
            item['mailState'] = ''
            item['mailZip'] = ''
        else:
            item['mailStreet'] = ''
            item['mailCity'] = ''
            item['mailState'] = ''
            item['mailZip'] = ''

        transFromTo = row[7].split('/ ')
        if len(transFromTo) == 0:
            item['transFrom'] = ""
            item['transTo'] = ""
        elif len(transFromTo) == 1:
            item['transFrom'] = transFromTo[0].strip()
            item['transTo'] = ""
        elif len(transFromTo) == 2:
            item['transFrom'] = transFromTo[0].strip()
            item['transTo'] = transFromTo[1].strip()

        item['geoCode'] = row[11]
        data.append(item)

 
if __name__ == "__main__":

    def upload_data():
        conn = db.get_db()
        query = f'''INSERT INTO status_changes(
            lic_num,
            status_from,
            status_to,
            lic_type,
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
            geocode
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''



        for item in data:
            args = []
            args.append(item['licNumber'])
            args.append(item['statusFrom'])
            args.append(item['statusTo'])
            args.append(item['licType'])
            args.append(item['issueDate'])
            args.append(item['expDate'])
            args.append(item['acctName'])
            args.append(item['acctOwn'])
            args.append(item['acctStreet'])
            args.append(item['acctCity'])
            args.append(item['acctState'])
            args.append(item['acctZip'])
            args.append(item['mailStreet'])
            args.append(item['mailCity'])
            args.append(item['mailState'])
            args.append(item['mailZip'])
            args.append(item['transFrom'])
            args.append(item['transTo'])
            args.append(item['geoCode'])

            try:
                cursor = conn.cursor()
                cursor.execute(query, args)

                if cursor.lastrowid:
                    print('Last Insert ID: ', cursor.lastrowid)
                else:
                    print('Last Insert ID Not Found!')

                conn.commit()
            
            except Error as e:
                print(e)
        
        print('Upload complete!')

        conn.close()

    upload_data()