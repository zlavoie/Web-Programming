import sys
import logging
from user import User

class UserDao:
    def __init__(self):
        self.filename = "UserIdPass.txt"

    def readUsers(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        
        result = []
        with open(self.filename, 'r') as file:
            # read the file into lines
            lines = file.readlines() 
            #logger.debug('line:%s',lines)
            # iterate through lines, splitting each line into strings
            for line in lines:
                raw = line.split()
                user = self.rowToUser(raw)
                result.append(user)
                
            return result
                
    def writeUsers(self,users):
        with open(self.filename, 'w') as file:
            # iterate through users, combining each attribute into a line
            for user in users:
                line = self.userToRow(user)
                file.write(line)
                
            file.close()
    
    def rowToUser(self,row):
        user = User(row[0], row[1])
        return user

    def userToRow(self,user):
        row = user.userid + "," + user.password
        return row

    def selectByUserId(self,userid):
        FORMAT="[%(filename)s:%(lineno)s - %(funName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        
        users  = self.readUsers()
        for user in users:
       #     logger.debug('userid:%s',user.userid)
            if (user.userid==userid):
        #        logger.debug('FOUND USER')
                return user
       # logger.debug('USER NOT FOUND')
        return None

    def selectAll(self):
        result = self.readUsers()
        return result
        
    def insert(self,user):
        users = self.readUsers()
        users.append(user)
        self.writeUsers(users)

    def update(self,user):
        self.deleteUser(user)
        users = self.readUsers()
        users.append(user)
        self.writeUsers(users)

    def delete(self,user):
        users = self.readUsers()

        for olduser in users:
            if (olduser.userid==userid):
                found = True
                break

        if (found is not True):
            print >> sys.stderr, "UserDao:update() unable to find user to delete userid " + userid
            return

        users.remove(olduser)
        self.writeUsers(users)

    def populate(self):
        users = []
        users.append(self.userToRow(User('bob','csrocks55')))
        users.append(self.userToRow(User('ralph','csrocks55')))
        users.append(self.userToRow(User('shai','csrocks55')))
        self.writeUsers(users)
