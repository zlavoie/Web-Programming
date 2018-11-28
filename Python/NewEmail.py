import cgi
import cgitb
import sys
import Cookie
import os
import random
        
def isValid(recepient):
    with open('UserIdPass.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            strings = iter(line.split())

            while True:
                try:
                    fileUserId=strings.next()
                    a=strings.next()
                    if(recepient==fileUserId):
                        return True
                except StopIteration:
                    break
    return False

def getEmails(recepient):
    result=[]
    with open((str(recepient)+".txt"), 'r') as file:
        lines=file.readlines()

        for line in lines:
            email=line.split(',')
            result.append(email)
    return result

def getEmail(emails,Num):
   for email in emails:
        if (email[1]==Num):
            return email
   return None

def main():
    cookie=Cookie.SimpleCookie()
    cookie_string=os.environ.get('HTTP_COOKIE')
    cookie.load(cookie_string)

    userid=cookie['userid'].value
    
    form=cgi.FieldStorage()
    new_message=form.getvalue('new_message')
    recepient=form.getvalue('recepient')
    subject=form.getvalue('subject')
    
    
    if isValid(recepient):
        emails=getEmails(recepient)
        cookie['recepient']=recepient
        cookie['subject']=subject
        cookie['userid']=userid
        cookie['new_message']=new_message
        idNum=10
        for email in emails:
            f=open((str(recepient)+".txt"),'a')
            f.write(str(subject)+","+str(idNum)+","+str(recepient)+","+str(new_message)+","+str(userid)+"\n")
            f.close()
            fout=open((str(userid)+"output.txt"),"a")
            fout.write(str(subject)+","+str(idNum)+","+str(recepient)+","+str(new_message)+","+str(userid)+"\n")
            fout.close()
        print "Content-type: text/html"
        print cookie.output()
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<meta http-equiv='Refresh' content='0; url=NewEmail.py' />"
        print "</head>"
        print "<body>"
        print "<p>Please follow <a href='NewEmail.py'>this link </a></p>"
        print "</body>"
        print "</html>"
        
    else:
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<head>"
        print "<title>Compose Message</title>"
        print "</head>"
        print "<html>"
        print "<body>"
        print "<h1>Compose A New Message</h1>"
        print
        print "<form id='form' action='NewEmail.py'  method='post'>"
        print "<h3><b>Subject:</b></h3> <input type='text' name='subject' />"
        print "<h3><b>To:</b></h3> <input type='text' name='recepient' />"
        print "<h3><b>Message:</b></h3> <textarea name='new_message'rows='20' cols='100' spellcheck='True'></textarea>"
        print "<br>"
                
        print "<p><button type='submit'>Send</button> | <button formaction='inbox.py'>Back To Inbox</button></p>"
        print "</body>"
        print "</html>"
        cookie['new_message']=new_message
main()
