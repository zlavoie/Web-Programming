#!/usr/bin/env python
import cgi
import sys
import Cookie
import os
import logging
from newview import NewView
from emaildao import EmailDao

class NewEmailController:    
    def __init__(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)

        cookie=Cookie.SimpleCookie()
        cookie_string=os.environ.get('HTTP_COOKIE')
        cookie.load(cookie_string)
        
        userid=cookie['userid'].value
        #If there was a form submission
        form=cgi.FieldStorage()
        new_message=form.getvalue('new_message')
        recepient=form.getvalue('recepient')
        subject=form.getvalue('subject')

        view=NewView()
        
        #if the person being send the email exists
        if (recepient is not None)and(new_message is not None):
#            logger.debug('we have a form submission. recepient: %s',recepient)
#            logger.debug('new message:%s',new_message)
            dao=EmailDao(userid) #get email dao
            emails=dao.selectAll() #get inbox emails
            found=dao.selectByRecepient #is the recepient found?
            if not dao.selectByRecepient(recepient):
                logger.debug('Made it to Invalid statement for user')
                view.Invalidview(new_message,recepient,subject,dao,emails)
            else:
                cookie['recepient']=recepient
                cookie['subject']=subject
                cookie['userid']=userid
                cookie['new_message']=new_message
                idNum=dao.determineId()
                newemail=subject+","+str(idNum)+","+recepient+","+new_message+","+userid
                logger.debug('Here is your email composition: %s',newemail)
                dao.insert(newemail)
                view.redirect()
        else:
            dao=EmailDao(userid)
            emails=dao.selectAll()
            view.view(new_message,recepient,subject,dao,emails)

controller=NewEmailController()
