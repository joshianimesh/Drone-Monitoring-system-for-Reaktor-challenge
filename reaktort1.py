import requests
import pandas as pd
import json
from pandas import json_normalize
import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime

df = pd.DataFrame()
class backend(object):
    def sqlconn(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd = '1234',
            database = 'reaktorchallenge')

        self.mycursor = self.db.cursor()
        return self.mycursor

    def getOffenders(self):

        self.srlist = []
        self.distXlist = []
        self.distYlist = []
        self.distCombined = []
        #getting API response
        response = requests.get(f"https://assignments.reaktor.com/birdnest/drones"     
        )
        tree = ET.fromstring(response.text)
        #print(response.text)
        #****print(tree[1][0][2])****
       
        for offenders in tree.findall('./capture/drone'):
            #print(offenders.find('positionX').text)
            print()
            if float(offenders.find('positionX').text) >=150000 and float(offenders.find('positionX').text) <=350000:
                if float(offenders.find('positionY').text) >=150000 and float(offenders.find('positionY').text) <=350000:
                    
                    
                    a = offenders.find('serialNumber').text
                    self.srlist.append(a)
                    x = offenders.find('positionX').text
                    self.distXlist.append(x)
                    y = offenders.find('positionY').text
                    self.distYlist.append(y)
                    distcombstring = str(x)+","+ str(y)
                    self.distCombined += [distcombstring]
                    
        #print(self.distCombined)
        return self.srlist

    def getPilotInfo(self):
        drone = self.srlist
        self.name = []
        self.phone = []
        self.email = []

        #print(drone)
        for i in drone:
            print(i)
            response = requests.get(f"https://assignments.reaktor.com/birdnest/pilots/{i}")
            data = response.json()
            #print(data)
            name1= data['firstName'] + ' ' + data['lastName']
            self.name += [name1]
            self.phone += [data['phoneNumber']]
            self.email += [data['email']]
             

    def commitmentsux(self):
         if len(self.srlist)>=1:
            for i in range(0,len(self.srlist)):
                srno = self.srlist[i]
                dist = self.distCombined[i]
                nameex = self.name[i]
                phoneno = self.phone[i]
                emailid = self.email[i]
                time = datetime.now()

                time_now = str(time.strftime("%H:%M:%S"))
                print(time_now)

                self.mycursor.execute("INSERT INTO offenders (Time, SerialNo, name, email, distance, phoneNumber) VALUES (%s,%s,%s,%s,%s,%s)",(time_now,srno,nameex,emailid,dist,phoneno))
                self.db.commit()
         elif len(self.srlist)==0:
            pass



class1 = backend()
class1.sqlconn()
class1.getOffenders()
class1.getPilotInfo()
class1.commitmentsux()


