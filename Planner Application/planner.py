from jsonpickle import encode
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
from flask import jsonify
from task import Task
import logging
import datetime
from taskdao import TaskDao
from userdao import UserDao
from user import User

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if ('login' in request.form):
        if isValid(request.form['userid'],request.form['password']):
            # Get the books from data store
            return redirect(url_for('TaskList'))
#            return TaskList()
        else:
            error = 'Invalid userid/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    elif ('SignUp' in request.form):
        return redirect(url_for('NewUser'))
    return render_template('login.html', error=error)

def isValid(userid, password):
    dao = UserDao()
    user = dao.selectByUserid(userid)
    if (user is not None) and (userid == user.userid) and (password == user.password):
        now=datetime.datetime.now()
        session['printM']=now.month
        if (len(str(session['printM']))<2):
            session['printM']=str(str(session['printM']).zfill(2))
        session['printD']=now.day
        if (len(str(session['printD']))<2):
            session['printD']=str(str(session['printD']).zfill(2))
        session['printY']=now.year
        
        if (len(str(session['printY']))<2):
            session['printY']=str(session['printY']).zfill(2)
        
        date=session['printM']+"-"+str(session['printD'])+"-"+str(session['printY'])
        session['currentdate']=date
#        print("DATE:"+viewdate)
        session['user']=encode(userid) # use an encoder to convert user to a JSON object for session
        return True
    else:
        return False

    #To main Task List Page
@app.route('/TaskList', methods=['POST', 'GET'])
def TaskList():
    dao = TaskDao()
    username=session['user']
    username=username.replace('"','')
    viewdate=session['currentdate']
    tasks = dao.selectByUserID(str(username))
    #taskArray=request.form.get('identifier')
    if ('Add' in request.form):
        return redirect(url_for('AddTask'))
    if ('CompleteList' in request.form):
        return redirect(url_for('CompleteList'))
   # if (taskArray is not None):
    if ('Completed' in request.form):
        taskArray=request.form['Completed']
        dao.CompletedTask(taskArray)      
        return redirect(url_for('TaskList'))
    elif ('Delete' in request.form):
        taskArray=request.form['Delete']
        dao.deleteTask(taskArray)
        return redirect(url_for('TaskList'))
    elif ('Show' in request.form):
        taskArray=request.form['Show']
        session['selected']=taskArray
        return redirect(url_for('ExamineTask'))
    elif('Edit' in request.form):
        taskArray=request.form['Edit']
        session['selected']=int(taskArray)
        return redirect(url_for('EditTask'))
    elif(('submitDate' in request.form)and(request.form['datepick']!= "")):
        session['currentdate']=request.form['datepick']
        date=session['currentdate']
        #print("Date in submitDate:"+str(date))
        printY=date.split('-',1)[0]
        printM=date.split('-',2)[1]
        printD=date.split('-',1)[1]
        printD=printD.split('-',1)[1]
        session['currentdate']=str(printM)+"-"+str(printD)+"-"+str(printY)
        return redirect(url_for('TaskList'))
    return render_template('ListView.html', **locals())

@app.route('/EditTask', methods=['POST', 'GET'])
def EditTask():
    dao=TaskDao()
    selected=dao.selectBytaskNum(int(session['selected']))
    duedate=selected.duedate
    session['printMs']=duedate.split('-',1)[0]
    session['printDs']=duedate.split('-',2)[1]
    session['printYs']=duedate.split('-',1)[1]
    session['printYs']=session['printYs'].split('-',1)[1]
    print(session['printYs'])
    if('submit' in request.form):
        dao.deleteTask(session['selected'])
        idNum=dao.determineId()
        username=session['user']
        username=username.replace('"','')
        task=request.form['task']
        duedate=request.form['duedate']
        session['printYs']=duedate.split('-',1)[0]
        session['printMs']=duedate.split('-',2)[1]
        session['printDs']=duedate.split('-',1)[1]
        session['printDs']=session['printDs'].split('-',1)[1]
        duedate=(str(session['printMs'])+"-"+str(session['printDs'])+"-"+str(session['printYs']))
        description=request.form['description']
#        print("past decsription")
        category=request.form['drop']
        priority=request.form['priority']
        newTask=Task(str(task),str(duedate),str(description),str(category),str(idNum),str(username),str(session['currentdate']),str(False),str(priority)) 
        dao.insert(newTask)
        return redirect(url_for('TaskList'))
    elif ('cancel' in request.form):
        return redirect(url_for('TaskList'))
    return render_template('EditTask.html', **locals())
    
@app.route('/ExamineTask', methods=['POST', 'GET'])
def ExamineTask():
    number=session['selected']
    dao=TaskDao()
    selected=dao.selectBytaskNum(number)
    if ('back' in request.form):
        return redirect(url_for('TaskList'))
    return render_template('ExamineTask.html', **locals())
    
@app.route('/CompleteList', methods=['POST', 'GET'])
def CompleteList():
    dao = TaskDao()
    username=session['user']
    username=username.replace('"','')
    viewdate=session['currentdate']
    viewdate=viewdate.replace('"','')
    viewdate=str(viewdate)
    
    tasks = dao.selectByCompleted(str(username))
    #taskArray=request.form.getlist('identifier')
    if ('Delete' in request.form):
        taskArray=request.form['Delete']
        session['selected']=taskArray
        dao.deleteTask(taskArray)
        return redirect(url_for('CompleteList'))
    elif('Back' in request.form):
        return redirect(url_for('TaskList'))
    elif ('Show' in request.form):
        taskArray=request.form['Show']
        session['selected']=taskArray
        return redirect(url_for('ExamineTaskCompleted'))
    return render_template('CompleteView.html', **locals())


@app.route('/ExamineTaskCompleted', methods=['POST', 'GET'])
def ExamineTaskCompleted():
    number=session['selected']
    dao=TaskDao()
    selected=dao.selectBytaskNum(number)
    if ('back' in request.form):
        return redirect(url_for('CompleteList'))
    return render_template('ExamineTaskCompleted.html', **locals())

@app.route('/NewUser', methods=['POST', 'GET'])
def NewUser():
    dao=UserDao()
    error = None
    #print("Here")
    if('Register' in request.form):
        user=dao.selectByUserid(request.form['newuserid'])
        print(user)
        if (request.form['newpassword']==request.form['verifypassword']):
            if  (user is None) and (request.form['newuserid'] != user):
                dao.insertNew(request.form['newuserid'],request.form['newpassword'])
                return redirect(url_for('login'))
            else:
                #passwords do not match
                error=1
                return render_template('NewUser1.html',error=error)
        elif (user is not None) and (request.form['newuserid'] != user.userid):
            #Username is already taken
            error=2
            return render_template('NewUser1.html',error=error)
    if('Login' in request.form):
        return redirect(url_for('login'))
    return render_template('NewUser1.html', error=error)

@app.route('/AddTask', methods=['GET', 'POST'])
def AddTask():
    #Add task to current day
    error = None
    dao=TaskDao()
    if ('submit' in request.form):
        idNum=dao.determineId()
        username=session['user']
        username=username.replace('"','')
        #now=datetime.datetime.now()
   

        task=request.form['task']
        duedate=request.form['duedate']
        printY=duedate.split('-',1)[0]
        printM=duedate.split('-',2)[1]
        printD=duedate.split('-',1)[1]
        printD=printD.split('-',1)[1]
        
        duedate=str(printM)+"-"+str(printD)+"-"+str(printY)
        
        description=request.form['description']
#        print("past decsription")
        category=request.form['drop']
        priority=request.form['priority']
        newTask=Task(str(task),str(duedate),str(description),str(category),str(idNum),str(username),str(session['currentdate']),str(False),str(priority)) 
        dao.insert(newTask)
#        print("DONE")
        return redirect(url_for('TaskList'))
    return render_template('AddTask.html', error=error)    
    
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', debug=True)
