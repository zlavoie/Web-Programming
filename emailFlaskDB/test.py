import dataset
from idnum import IdNum
from emails import Email
from flask import current_app
import sys
import random
from flask import Flask
from flask import session
class EmailDao:
    def __init__(self):
#        self.connectString = 'sqlite:///'+str(session['userid'])+'emails.db'
#        self.db = dataset.connect(self.connectString)
#        self.table = self.db[(str(session['userid'])+'emails')]
        
#        self.connectString= 'sqlite:///'+str(session['userid'])+'outbox.db'
#        self.db1= dataset.connect(self.connectString)
#        self.table1= self.db1[(str(session['userid'])+'outbox')]
        
#        self.connectString= 'sqlite:///'+str(session['userid'])+'trash.db'
#        self.db2= dataset.connect(self.connectString)
#        self.table2= self.db2[(str(session['userid'])+'trash')]

        self.connectString = 'sqlite:///zoeemails.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['emails']       
        self.connectString= 'sqlite:///zoeoutbox.db'
        self.db1= dataset.connect(self.connectString)
        self.table1= self.db1['outbox']
        
        self.connectString= 'sqlite:///zoetrash.db'
        self.db2= dataset.connect(self.connectString)
        self.table2= self.db2['trash']

        
        self.connectString= 'sqlite:///IdNum.db'
        self.db3= dataset.connect(self.connectString)
        self.table3=self.db2['IdNum']
        
    def rowToEmail(self,row):
        email = Email(row['subject'], row['Num'], row['recepient'], row['message'],row['sender'])
        return email

    def emailToRow(self,email):
        row = dict(subject=email.subject, Num=email.Num, recepient=email.recepient, message=email.message,sender=email.sender)
        return row

    def NumToRow(self,number):
        row = dict(Num1=number.Num1)
        return row
    
    
    def selectByNum(self,Num,types):
        if (types == 0):
            table=self.db['emails']
            rows   = self.table.find(Num=Num)
        elif (types==1):
            table1=self.db1['outbox']
            rows   = self.table1.find(Num=Num)
        elif (types==2):
            table2=self.db2['trash']
            rows   = self.table2.find(Num=Num)
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
        
    def selectAll(self):
        table = self.db['emails']
        rows   = table.all()
        result = []
        for row in rows:
            result.append(self.rowToEmail(row))
        return result

    def selectAllOutbox(self):
        table1 = self.db1['outbox']
        rows   = table1.all()

        result = []
        for row in rows:
            result.append(self.rowToEmail(row)) 
        return result

    def selectAllTrash(self):
        table2 = self.db2['trash']
        rows   = table2.all()

        result = []
        for row in rows:
            result.append(self.rowToEmail(row))

        return result

    def determineId(self):
        table3=self.db3['IdNum']
    
        Number=random.randint(1,10000)
        
        self.table3.insert(self.NumToRow(IdNum(str(Number))))
        self.db3.commit()
        return Number

    def insert(self,email):
        self.table.insert(self.emailToRow(email))
        self.db.commit()

    def insertOutbox(self,email):
        self.table1.insert(self.emailToRow(email))
        self.db1.commit()

    def update(self,email):
        self.table.update(self.emailToRow(email),['Num'])
        self.db.commit()
        
    def delete(self,email):
        self.table2.insert(self.emailToRow(email))
        self.db2.commit()
        
        self.table.delete(Num=email.Num)
        self.db.commit()

    def deleteOutbox(self,email):
        self.table2.insert(self.emailToRow(email))
        self.db2.commit()
        
        self.table1.delete(Num=email.Num)
        self.db1.commit()

    def deleteTrash(self,email):
        self.table2.delete(Num=email.Num)
        self.db2.commit()
        
    def populate(self):
        #populates inbox
        self.table.insert(self.emailToRow(Email('Help With Programming','12','zoe','Will you come over to the suite tomorrow and help me with a programming assignment?','chris')))
        self.table.insert(self.emailToRow(Email('Dinner Tonight','102','zoe','Do you want to go off campus tonight to grab dinner?','tony')))
        self.table.insert(self.emailToRow(Email('Happy Birthday!','40','zoe','Happy 21st birthday! We should go out and grab drinks later!','tony')))
        self.table.insert(self.emailToRow(Email('Thai Food','265','zoe','Do you want to go to Ruk Mai down the street to get Pad Thai and maybe some shrimp fried rice?','tony')))
        self.table.insert(self.emailToRow(Email('Self Note','93','zoe','Remember to finish your email system it is due on Friday for web prograaming class','zoe')))
        self.db.commit()

    def populateNew(self,username):
        #populates inbox
        Num =self.determineId()
        self.table.insert(self.emailToRow(Email('Welcome',str(Num),str(username),'Welcome To Zmail! We are so glad to have you be a part of our community!','Zmail Team')))
        self.db.commit()

    def populate1New(self,username):
        #populates new outbox
        Num = self.determineId()
        self.table.insert(self.emailToRow(Email('Welcome',str(Num),str(username),'This is your outbox where you can see all the messages you have sent.','Zmail Team')))
        self.db.commit()

    def populate2New(self,username):
        #populates inbox
        Num = self.determineId()
        self.table.insert(self.emailToRow(Email('Welcome',str(Num),str(username),'This is your trash. This is where all the deleted messages from your outbox and inbox come to until you delete them forever.','Zmail Team')))
        self.db.commit()
   
    def populate1(self):
        #populates outbox

        self.table1.insert(self.emailToRow(Email('Ice Cream','39','chris','Would you want to go to Daddy Dairy on Friday Night?','zoe')))
        self.table1.insert(self.emailToRow(Email('Frisbee','10','chris','I am not going to be able to go to frisbee practive on Tuesday night','zoe')))
        self.table1.insert(self.emailToRow(Email('Birthday Gift','138','chris','What should we get Erin for her birthday? I have no clue and I have been looking all over amazon.','zoe')))
        self.table1.insert(self.emailToRow(Email('Computer Science','17','chris','I am bored in class','zoe')))
        self.table1.insert(self.emailToRow(Email('Bachelor','827','tony','Do you want to watch the Bachelor on Sunday night? It is almost the season finale!','zoe')))
        self.db1.commit()

    
    def populate2(self):
        #populates trash
        self.table2.insert(self.emailToRow(Email('Welcome!','1234','chris','Welcome to Zmail! So glad you can join our community! ','zmail')))
        self.db2.commit()

    def populate3(self):
        #populates IdNum
       self.table3.insert(self.NumToRow(IdNum('39')))

       self.table3.insert(self.NumToRow(IdNum('138')))
       self.table3.insert(self.NumToRow(IdNum('273')))
       self.table3.insert(self.NumToRow(IdNum('98')))
       self.table3.insert(self.NumToRow(IdNum('10')))
       self.table3.insert(self.NumToRow(IdNum('687')))
       self.table3.insert(self.NumToRow(IdNum('13')))
       self.table3.insert(self.NumToRow(IdNum('349')))
       self.table3.insert(self.NumToRow(IdNum('9')))
       self.table3.insert(self.NumToRow(IdNum('224')))

        self.table3.insert(self.NumToRow(IdNum('102')))
        self.table3.insert(self.NumToRow(IdNum('40')))
        self.table3.insert(self.NumToRow(IdNum('265')))
        self.table3.insert(self.NumToRow(IdNum('93')))
        self.table3.insert(self.NumToRow(IdNum('17')))
        self.table3.insert(self.NumToRow(IdNum('827')))
        self.db3.commit()
