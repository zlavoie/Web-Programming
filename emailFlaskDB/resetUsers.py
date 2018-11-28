from emaildao import EmailDao
from emails import Email
from userdao import UserDao
from user import User
import os
import logging
from flask import Flask
from flask import session
        
#repopulates users
os.remove('users.db')
dao = UserDao()
dao.populate()
users = dao.selectAll()
for user in users:
    print (user.toString())
