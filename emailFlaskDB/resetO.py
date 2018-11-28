from emaildao import EmailDao
from emails import Email
from userdao import UserDao
from user import User
import os
import logging
from flask import Flask
from flask import session

#repopulates users
#os.remove('users.db')
#dao = UserDao()
#dao.populate()
#users = dao.selectAll()
#for user in users:
#    print (user.toString())

os.remove('zoeemails.db')
dao = EmailDao()
dao.populate()
emails = dao.selectAll()
print emails
for email in emails:
    print(email.toString())

#populates outbox
os.remove('zoeoutbox.db')
dao = EmailDao()
dao.populate1()
emails = dao.selectAllOutbox()
for email in emails:
    print(email.toString())

#populates trash
os.remove('zoetrash.db')
dao = EmailDao()
dao.populate2()
emails = dao.selectAllTrash()
for email in emails:
    print(email.toString())
