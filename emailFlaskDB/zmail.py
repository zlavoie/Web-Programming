from jsonpickle import encode
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from emails import Email
from userdao import UserDao
from user import User
from resetdb import ResetDB
from inboxdao import InboxDao
from outboxdao import OutboxDao
from trashdao import TrashDao

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    
    if('submit' in request.form) and ('userid' in request.form) and ('password' in request.form):
        userid=request.form['userid']
        if isValid(request.form['userid'],request.form['password']):
            session['userid']=request.form['userid']
            return inbox()
        else:
            error = 'Invalid userid/password'
    elif('submit2' in request.form) and (request.form['passwordNew'] is not None) and (request.form['useridNew'] is not None):
        if not (isValid(request.form['useridNew'],request.form['passwordNew'])):
            dao=UserDao()
            #insert into datbase
            dao.insertNew(request.form['useridNew'],request.form['passwordNew'])
            #create datbase files for user
            f=open((str(request.form['useridNew'])+"emails.db"),"w+")
            f=open((str(request.form['useridNew'])+"outbox.db"),"w+")
            f=open((str(request.form['useridNew'])+"trash.db"),"w+")
            session['userid']=request.form['useridNew']
            ResetDB(str(request.form['useridNew']))
            session.clear()
            f.close()
            return redirect(url_for('login'))
    return render_template('login.html', error=error)


def isValid(userid, password):
    dao = UserDao()
    user = dao.selectByUserId(userid)
    if (user is not None) and (userid == user.userid) and (password == user.password):
        session['user']=encode(user)
        return True
    else:
        return False

def isValidRecepient(userid):
    dao = UserDao()
    user = dao.selectByUserId(userid)
    if (user is not None) and (userid == user.userid):
        return True
    else:
        return False

@app.route('/delete', methods=['POST', 'GET'])
def delete(Num):
    dao=InboxDao()
    email=dao.selectByNum(Num)
    dao.delete(email)
    return redirect(url_for('inbox'))

@app.route('/inbox', methods=['POST', 'GET'])
def inbox():
    dao=InboxDao()
    emails=dao.selectAll()
    if ('outbox' in request.form):
        return redirect(url_for('outbox'))
    elif ('inbox' in request.form):
        return redirect(url_for('inbox'))
    elif ('trash' in request.form):
        return redirect(url_for('trash'))
    elif ('readE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        return readInbox(Num)
    elif ('deleteE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        return delete(Num)
    elif ('newE' in request.form):
        return redirect(url_for('newMessage'))
    elif('LogE' in request.form):
        session.clear()
        return redirect(url_for('login'))
    else:
        app.logger.debug('In the Inbox')
        return render_template('inbox.html', **locals() )

@app.route('/readInbox', methods=['POST', 'GET'])
def readInbox(Num):
    dao=InboxDao()
    email=dao.selectByNum(Num)
    if ('back' in request.form):
        return redirect(url_for('inbox'))
    return render_template('readInbox.html', **locals())

@app.route('/newMessage', methods=['POST', 'GET'])
def newMessage():
    dao=OutboxDao()
    if ('back' in request.form):
        return redirect(url_for('inbox'))
    if ('submit' in request.form):
        if (request.form['recepient'] is not None) and (request.form['new_message'] is not None):
            if (isValidRecepient(request.form['recepient'])):
                idNum=dao.determineId()
                newemail=Email(str(request.form['subject']),str(idNum),str(request.form['recepient']),str(request.form['new_message']),str(session['userid']))
                
                dao.insertOutbox(newemail)
                #also submit into other users inbox
                #dao.ToRecepient(newemail)
                return redirect(url_for('outbox'))
            else:
                return render_template('invalidview.html', **locals())
    return render_template('newMessage.html', **locals())


@app.route('/readOutbox', methods=['POST', 'GET'])
def readOutbox(Num):
    dao=OutboxDao()
    email=dao.selectByNum(Num)
    if ('back' in request.form):
        return redirect(url_for('outbox'))
    return render_template('readOutbox.html', **locals())
    
    
@app.route('/outbox', methods=['POST', 'GET'])
def outbox():
    app.logger.debug('in the outbox')
    dao=OutboxDao()
    emails=dao.selectAllOutbox()
    if ('outbox' in request.form):
        return redirect(url_for('outbox'))
    elif ('inbox' in request.form):
        return redirect(url_for('inbox'))
    elif ('trash' in request.form):
        return redirect(url_for('trash'))
    elif ('readE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        return readOutbox(Num)
    elif ('deleteE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        app.logger.debug('deleting out of the outbox area')
        return deleteOutbox(Num)
    elif ('newE' in request.form):
        return redirect(url_for('newMessage'))
    elif('LogE' in request.form):
        session.clear()
        return redirect(url_for('login'))
    return render_template('outbox.html', **locals() )


@app.route('/deleteOutbox', methods=['POST', 'GET'])
def deleteOutbox(Num):
    dao=OutboxDao()
    email=dao.selectByNum(Num)
    dao.deleteOutbox(email)
    return redirect(url_for('outbox'))


@app.route('/deleteTrash', methods=['POST', 'GET'])
def deleteTrash(Num):
    dao=TrashDao()
    email=dao.selectByNum(Num)
    dao.deleteTrash(email)
    return redirect(url_for('trash'))


@app.route('/readTrash', methods=['POST', 'GET'])
def readTrash(Num):
    dao=TrashDao()
    email=dao.selectByNum(Num)
    if ('back' in request.form):
        return redirect(url_for('trash'))
    return render_template('readTrash.html', **locals())
    
    
@app.route('/trash', methods=['POST', 'GET'])
def trash():
    app.logger.debug('made it to the trash')
    dao=TrashDao()
    emails=dao.selectAllTrash()
    if ('outbox' in request.form):
        return redirect(url_for('outbox'))
    elif ('inbox' in request.form):
        return redirect(url_for('inbox'))
    elif ('trash' in request.form):
        return redirect(url_for('trash'))
    elif ('readE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        return readTrash(Num)
    elif ('deleteE' in request.form) and ('Num' in request.form):
        Num=request.form['Num']
        app.logger.debug('deleting in the Trash area')
        return deleteTrash(Num)
    elif('LogE' in request.form):
        session.clear()
        return redirect(url_for('login'))
    return render_template('trash.html', **locals() )

    
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    streamhandler = logging.StreamHandler(sys.stderr)
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(Formatter("[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"))
    app.logger.addHandler(streamhandler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0')
