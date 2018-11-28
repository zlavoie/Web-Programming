from taskdao import TaskDao
from userdao import UserDao
from task import Task
from user import User
import os

os.remove('users.db')
dao = UserDao()
dao.populate()
users = dao.selectAll()
for user in users:
   print(user.toString())
os.remove('task.db')
dao = TaskDao()
#dao.populate()
#tasks = dao.selectAll()
#for task in tasks:
#   print(task.toString())
