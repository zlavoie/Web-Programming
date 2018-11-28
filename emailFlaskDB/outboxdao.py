import dataset
from idnum import IdNum
from emails import Email
from flask import current_app
import sys
import random
import logging
from flask import Flask
from flask import session
from trashdao import TrashDao
class OutboxDao:
    def __init__(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        self.connectString= str('sqlite:///'+str(session['userid'])+'outbox.db')
        self.db1= dataset.connect(self.connectString)
        self.table1= self.db1['outbox']
        
        self.connectString= 'sqlite:///IdNum.db'
        self.db3= dataset.connect(self.connectString)
        self.table3=self.db3['IdNum']
        
    def rowToEmail(self,row):
        email = Email(row['subject'], row['Num'], row['recepient'], row['message'],row['sender'])
        return email

    def emailToRow(self,email):
        row = dict(subject=email.subject, Num=email.Num, recepient=email.recepient, message=email.message,sender=email.sender)
        return row

    def NumToRow(self,number):
        row = dict(Num1=number.Num1)
        return row
    
    def selectByNum(self,Num):
        table1=self.db1['outbox']
        rows   = self.table1.find(Num=Num)
        result=''
        if (rows is None):
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
      
                    return None
                else:
                    result = self.rowToEmail(row)
                    count = count + 1
        return result
        
    def selectAllOutbox(self):
        table1 = self.db1['outbox']
        rows   = table1.all()

        result = []
        for row in rows:
            result.append(self.rowToEmail(row)) 
        return result
    def determineId(self):
        table3=self.db3['IdNum']
        Number=random.randint(1,10000)
        if(self.table3.find(Number)):
            n1 = Number
            while(n1==Number):
                Number=random.randint(1,10000)
                
        self.table3.insert(self.NumToRow(IdNum(str(Number))))
        self.db3.commit()
        return Number

    def insertOutbox(self,email):
        self.table1.insert(self.emailToRow(email))
        self.db1.commit()

    def deleteOutbox(self,email):
        dao=TrashDao()
        dao.insertTrash(email)
        
        self.table1.delete(Num=email.Num)
        self.db1.commit()
