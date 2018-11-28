#!/usr/bin/env python
 
import Cookie
import cgi
import logging
from userdao import UserDao
from loginview import LoginView

class LoginController:
    def __init__(self):
        FORMAT="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
        logging.basicConfig(filename='output.log',format=FORMAT)
        logger=logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        
        #If there was a form submitted save the values
        form = cgi.FieldStorage() 
        userid   = form.getvalue('userid')
        password = form.getvalue('password')
        
        useridNew = form.getvalue('useridNew')
        passwordNew = form.getvalue('passwordNew')
        space = " "

        #setup view
        view = LoginView()

            #Checks to see if login is valid       
        if self.isValid(userid,password):
            logger.debug('Username and password are valid, access granted')
            cookie = Cookie.SimpleCookie()
            cookie['userid']=userid
            view.redirect(cookie)
        logger.debug('username fail:%s',userid)
        logger.debug('password fail:%s',password)
        if (useridNew is not None) and (passwordNew is not None):
            logger.debug('Did not make it to validity')
        #Deciding If New User Is Valid
        #create Inbox, outbox,trash
            if not(self.isValid(useridNew,passwordNew)):
                logger.debug('Usernam andpassword are not vaild')
#NEED TO CHANGE THIS CHUNK TO WORK WITH USERDAO  
                f=open("UserIdPass.txt","a")
                f.write(str(useridNew)+" "+str(passwordNew)+"\n")
                f.close()
               # #write the new user a file to hold their email information
                f=open((str(useridNew)+".txt"),"w+")
               #write the new user a file to hold their sent messages
                f=open((str(useridNew)+"output.txt"),"w+")
                f=open((str(useridNew)+"trash.txt"),"w+")
                f.close()
        else:
            view.view()

    def isValid(self,userid, password):
        dao=UserDao()
        user=dao.selectByUserId(userid)
        if user is not None:
            if (user.password==password):
               # logger.debug('isvalid is true')
                return True
        else:
           # logger.debug('is valid is false')
            return False
controller=LoginController()
