import logging
import random
from email import Email

class EmailDao:
    def __init__(self,userid):
        self.filename = userid+".txt"
        self.filename2=userid+"output.txt"
        self.filename3=userid+"trash.txt"
    def readEmails(self):
        result = []
        with open(self.filename, 'r') as file:
            # read the file into lines
            lines = file.readlines() 
            
            # iterate through lines, splitting each line into strings
            for line in lines:
                raw = line.split(',')
                email = self.rowToEmail(raw)
                result.append(email)
                
        return result
                
    def writeEmails(self,emails):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        with open(self.filename, 'w') as file:
            # iterate through books, combining each attribute into a line
            for email in emails:
                line = self.emailToRow(email)
#                logger.debug('Line: %s',line)
                file.write(line)                
            file.close()

    def determineId(self):
        emails=self.readEmails()
        idNum=random.sample(range(1000),1)
        for email in emails:
            while (email.Num==idNum):
                for x in range(1):
                    idNum=random.randint(1,1000)
        return idNum
            
    def rowToEmail(self,row):    
        email = Email(row[0], row[1], row[2],row[3],row[4])
        return email

    def emailToRow(self,email):
        row = email.subject+ "," + email.Num+ "," +email.recepient + "," +email.message+","+ email.sender
        return row


    def selectByRecepient(self,recepient):
        emails  = self.readEmails()
        for email in emails:
            if (email.recepient==recepient):
                return True
                            
        return False


    def selectSent(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        result = []
        with open(self.filename2, 'r') as file:
            # read the file into lines
            lines = file.readlines() 
            # iterate through lines, splitting each line into strings
            for line in lines:
                raw = line.split(',')
#                logger.debug('here is the line: %s',raw)
                email = self.rowToEmail(raw)
                result.append(email)                
            return result

    def selectTrash(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        result = []
        with open(self.filename3, 'r') as file:
            # read the file into lines
            lines = file.readlines() 
            # iterate through lines, splitting each line into strings
            for line in lines:
                raw = line.split(',')
#                logger.debug('here is the line: %s',raw)
                email = self.rowToEmail(raw)
                result.append(email)                
            return result        
        
    def selectByNum(self,Num):
        emails  = self.readEmails()
        for email in emails:
            if (email.Num==Num):
                return email
                            
        return None

    def selectByNumSent(self,Num):
        emails  = self.selectSent()
        for email in emails:
            if (email.Num==Num):
                return email
                            
        return None

    def selectByNumTrash(self,Num):
        emails  = self.selectTrash()
        for email in emails:
            if (email.Num==Num):
                return email
                            
        return None

    
    def selectAll(self):
        result = self.readEmails()
        return result
        
    def insert(self,email):
        with open(self.filename,'a') as file:
            file.write(email)
        file.close()    

    def update(self,email):
        emails = self.readEmails()

        for oldemail in emails:
            if (oldemail.Num==email.Num):
                found = True
                break

        if (found is not True):
            print >> sys.stderr, "EmailDao:update() unable to find email to update isbn " + Num
            return

        emails.remove(oldemail)
        emails.append(email)
        self.writeBooks(emails)


    def deleteForever(self,Num,email,emails):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        with open (self.filename3,'w') as file:
            for emailnum in emails:
                if not((emailnum.Num)==(Num)):
                    line = self.emailToRow(emailnum)
                   # logger.debug('NUM:%s',Num)
                   # logger.debug('COMPARISOM:%s',emailnum.Num)
                    file.write(line)
               # else:
                   # logger.debug('A MATCH')
        file.close()

    def deleteOutbox(self,Num,email,emails):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        with open (self.filename2,'w') as file:
            for emailnum in emails:
                if not((emailnum.Num)==(Num)):
                    line = self.emailToRow(emailnum)
                   # logger.debug('NUM:%s',Num)
                   # logger.debug('COMPARISOM:%s',emailnum.Num)
                    file.write(line)
                else:
                    with open (self.filename3,'a') as f:
                        line=self.emailToRow(emailnum)
                        f.write(line)
                    f.close()
                   # logger.debug('A MATCH')
        file.close()

    def deleteInbox(self,Num,email,emails):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        with open (self.filename,'w') as file:
            for emailnum in emails:
                if not((emailnum.Num)==(Num)):
                    line = self.emailToRow(emailnum)
                   # logger.debug('NUM:%s',Num)
                   # logger.debug('COMPARISOM:%s',emailnum.Num)
                    file.write(line)
                else:
                    with open (self.filename3,'a') as f:
                        line=self.emailToRow(emailnum)
                        f.write(line)
                        f.close()
        file.close()
        
