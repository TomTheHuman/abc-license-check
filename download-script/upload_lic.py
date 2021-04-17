import csv

with open('./data/report.csv') as datafile:
    data = []
    dataReader = csv.reader(datafile)
    next(dataReader)
    for row in dataReader:
        item = {}
        item['licNumber'] = row[0]
        item['statusFrom'] = row[1][:(row[1].find(' '))]
        item['statusTo'] = row[1][(row[1].find(' ') + 1):]
        item['licType'] = row[2][:(row[2].find(' ') - 2)]
        item['issueDate'] = row[3]
        item['expDate'] = row[4]
        
        primOwnAddr = row[5].split('                        ')
        if(primOwnAddr[0][:3] == 'DBA'):
            item['acctName'] = primOwnAddr[0][5:]
            item['acctOwn'] = primOwnAddr[1]
            item['acctStreet'] = primOwnAddr[2][:-1]
            item['acctCityStateZip'] = primOwnAddr[3]
        else:
            item['acctOwn'] = primOwnAddr[0]
            item['acctStreet'] = primOwnAddr[1][:-1]
            item['acctCityStateZip'] = primOwnAddr[2]

        mailAddr = row[6].split('                              ')
        print(mailAddr[0])
        if len(mailAddr) > 1:
            item['mailStreet'] = mailAddr[0]
            item['mailCityStateZip'] = mailAddr[1]
        elif len(mailAddr) > 0:
            item['mailStreet'] = mailAddr[0]
            item['mailCityStateZip'] = ''
        else:
            item['mailStreet'] = ''
            item['mailCityStateZip'] = ''

        transFromTo = row[7].split('/ ')
        if len(transFromTo) == 0:
            item['transFrom'] = ""
            item['transTo'] = ""
        elif len(transFromTo) == 1:
            item['transFrom'] = transFromTo[0]
            item['transTo'] = ""
        elif len(transFromTo) == 2:
            item['transFrom'] = transFromTo[0]
            item['transTo'] = transFromTo[1]

        item['geoCode'] = row[11]
        data.append(item)

        print(f"Lic#: {item['licNumber']}, Type: {item['licType']}, Status From: {item['statusFrom']}, Status To: {item['statusTo']}, Issue Date: {item['issueDate']}, Exp. Date: {item['expDate']}, Account Street: {item['acctStreet']}, Account City, State, Zip: {item['acctCityStateZip']}, Mailing Street: {item['mailStreet']}, Mailing City, State, Zip: {item['mailCityStateZip']}, Transfer From: {item['transFrom']}, Transfer To: {item['transTo']}, GeoCode: {item['geoCode']}")

if __name__ == "__main__":
    
    def function:
        print("Function")

    
