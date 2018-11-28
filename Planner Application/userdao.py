import dataset
from user import User

class UserDao:
    def __init__(self):
        self.connectString = 'sqlite:///users.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['users']

    def rowToUser(self,row):
        user = User(row['userid'], row['password'])
        return user

    def userToRow(self,user):
        row = dict(userid=user.userid, password=user.password)
        return row

    def insertNew(self, userNew,passNew):
        self.table.insert(self.userToRow(User(str(userNew),str(passNew))))
        self.db.commit
    
    def selectByUserid(self,userid):
        rows   = self.table.find(userid=userid)
        result = None
        
        if (rows is None):
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    return None
                else:
                    result = self.rowToUser(row)
                    count = count + 1

        return result

    def selectAll(self):
        table = self.db['users']
        rows   = table.all()

        result = []
        for row in rows:
            result.append(self.rowToUser(row))

        return result
        
    def insert(self,user):
        self.table.insert(self.userToRow(user))
        self.db.commit()

    def update(self,user):
        self.table.update(self.userToRow(user),['userid'])
        self.db.commit()

    def delete(self,user):
        self.table.delete(userid=userid)
        self.db.commit()

    def populate(self):
        self.table.insert(self.userToRow(User('zlavoie','SkyHawk123')))
        self.table.insert(self.userToRow(User('bdugan','Professor123')))
        self.table.insert(self.userToRow(User('bbloom','Boland369')))
        self.db.commit()
