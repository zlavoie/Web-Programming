class Task:
    def __init__(self, task, duedate, description, category,taskNum,username,listdate,completed,priority):
        self.task = task
        self.duedate = duedate
        self.description=description
        self.category = category
        self.taskNum = taskNum
        self.username=username
        self.listdate=listdate
        self.completed=completed
        self.priority=priority
        
    def toString(self):
        return self.task + " " + self.duedate+ " " + self.description+ " " + self.category+" "+str(self.taskNum)+" "+self.username+" "+self.listdate + " "+self.completed+" "+str(self.priority)


