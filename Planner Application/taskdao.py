import dataset
import random
from flask import session
from task import Task
import datetime
from num import Num
class TaskDao:
    def __init__(self):
        self.connectString = 'sqlite:///task.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['task']

        self.connectString = 'sqlite:///Num.db'
        self.db2 = dataset.connect(self.connectString)
        self.table2 = self.db2['Num']

    def rowToTask(self,row):
        task = Task(row['task'], row['duedate'], row['description'], row['category'],row['taskNum'],row['username'],row['listdate'],row['completed'],row['priority'])
        return task

    def taskToRow(self,task):
        row = dict(task=task.task, duedate=task.duedate, description=task.description, category=task.category,taskNum=task.taskNum,username=task.username,listdate=task.listdate,completed=task.completed,priority=task.priority)
        return row

    def determineId(self):
        table2=self.db2['Num']
        Number=random.randint(1,10000)
        if(self.table2.find(Number)):
            n1=Number
            while(n1==Number)and(self.table2.find(Number)==False):
                Number=random.randint(1,10000)
        self.table2.insert(self.NumToRow(Num(str(Number))))
        self.db2.commit()
        return Number

    def NumToRow(self,number):
        row=dict(Num1=number.Num1)
        return row
    
    def insert(newTask):
        self.table.insert(self.taskToRow(newtask))
        self.db.commit()
    
    def selectByCompleted(self,username):
        table = self.db['task']
        rows   = table.all()
        result = []
        if (rows is None):
            result = None
        else:
            for row in rows:
                task=self.rowToTask(row)
                if(str(task.username) == str(username)):
                    if(task.completed != "False"):
                        result.append(self.rowToTask(row))
        return result


    def selectByUserID(self,username):
        table = self.db['task']
        rows   = table.all()
        result = []
        if (rows is None):
            result = None
        else:
            for row in rows:
                task=self.rowToTask(row)
                if(str(task.username) == str(username)):
                    if(task.completed != "True"):
                        if(task.listdate == session['currentdate']):
                            result.append(self.rowToTask(row))
        return result
    
    def selectBytaskNum(self,taskNum):
        rows   = self.table.find(taskNum=taskNum)
        result=None
        if (rows is None):
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    return None
                else:
                    result =  self.rowToTask(row)
                    count = count + 1

        return result

    def selectAll(self):
        table = self.db['task']
        rows   = table.all()
        result = []
        for row in rows:
            result.append(self.rowToTask(row))
        return result

    
    def insert(self,task):
        self.table.insert(self.taskToRow(task))
        self.db.commit()

    def update(self,task):
        self.table.update(self.taskToRow(task),['taskNum'])
        self.db.commit()

    def deleteTask(self,task):
        dao=TaskDao()
        print(task)
        task=dao.selectBytaskNum(task)
        self.table.delete(taskNum=task.taskNum)
        self.db.commit()

    def CompletedTask(self,task):
        dao=TaskDao()
        task=dao.selectBytaskNum(task)
        temptask=Task(str(task.task),str(task.duedate),str(task.description),str(task.category),str(task.taskNum),str(task.username),str(task.listdate),"True",str(task.priority))
        self.table.delete(taskNum=task.taskNum)
        self.table.insert(self.taskToRow(temptask))
        self.db.commit()
        
    def insert(self,task):
        self.table.insert(self.taskToRow(task))
        self.db.commit()

    def populate(self):
        now=datetime.datetime.now()
        self.table.insert(self.taskToRow(Task('Clean the suite','04-29-2018','Please clean the floor and tables','School','1','bdugan','04-20-2018','False','1')))
        self.table.insert(self.taskToRow(Task('Grade Homework','04-29-2018','Need to grade homework for programming languages','Work','2','bdugan','04-20-2018','False','2')))

        self.db.commit()
