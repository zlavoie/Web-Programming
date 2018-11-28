import cgi
import sys
import Cookie
import os

def getEmail(userid):
    result = []
    with open((str(userid)+".txt"), 'r') as file:
        # read the file into lines
        lines = file.readlines() 

        # iterate through lines, splitting each line into strings
        for line in lines:
            email = line.split(',')
            result.append(email)

    return result

#
# Main Program
#
def main():
    # get the cookie
    cookie = Cookie.SimpleCookie()
    cookie_string = os.environ.get('HTTP_COOKIE')
    cookie.load(cookie_string)
    userid = cookie['userid'].value

    # get the form submission if there was one
    form = cgi.FieldStorage() 
    Num=form.getvalue('Num')
    readE=form.getvalue('readE')
    deleteE=form.getvalue('deleteE')
    newE=form.getvalue('newE')
    
    if(Num is not None)or (newE is not None):
        cookie['Num']=Num
        cookie['readE']=readE
        cookie['deleteE']=deleteE
        cookie['newE']=newE        
        print "Content-type: text/html"
        print cookie.output()
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<meta http-equiv='Refresh' content='0; url=InboxAction.py' />"
        print "</head>"
        print "<body>"
        print "<p>Please follow <a href='InboxAction.py'>this link</a></p>"
        print "</body>"
        print "</html>"
        
        # first time on this page
    else:
       print "Content-type: text/html"
       print
       print "<!doctype html>"
       print "<head>"
       print "<title>Inbox</title>"
       print "</head>"
       print "<html>"
       print "<body>"
       print "<h1>Inbox</h1>"
       print "<h3>Welcome "+userid+" to your email account!</h3>"
       print "<p><a href='outbox.py'>Outbox</a> |  <a href='inbox.py'>Inbox</a> | <a href='trash.py'>Trash</a></p>"
       print "<form id='form' action='inbox.py'  method='post'>"
        
        # display list of emails depending on user that is logged in as radio buttons
       emails = getEmail(userid)
       for email in emails:
           print "      <input type='radio'  name='Num' value='"+email[1]+"'>" +"From: "+email[4] + "</br>"+"&emsp;&emsp;<b>" + email[0] +"</b> </br>"
           print "</br>"    
       print "   <input type='submit' id='Read_Email' name='readE' value='Read'/>"
       print "   <input type='submit' id='Delete_Email' name='deleteE' value='Delete'/>"
       print "   <input type='submit' formaction='NewEmail.py' id='New_Email' name='newE' value='New'/>"
       print "</form>"
       print
       print "</body>"
       print "</html>"        
main()
