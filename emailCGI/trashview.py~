#!/usr/bin/env python
 
import cgi
import sys
import Cookie
import os
        
class TrashView:
    def redirectRead(self,email):
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<link rel='stylesheet' type='text/css' href='./css/main.css'>"
        print "</head>"
        print "<br>"
        print "<div class='outter'>"
        print "<body class='inbox'>"
        print "<h1 class='inbox'>Trash Message</h1>"
        print "</div>"
        print "<br>"
        print "<div class='outter2'>"
        print "<form id='form' method='post' action='trashcontroller.py'>"
        print "<p class='trash'><b>From: </b>"+email.sender+"</p>"
        print "<p class='trash'><b>Subject: </b>"+email.subject+"</p>"
        print "</div>"
        print "<br>"
        print "<textarea rows='20' cols='102' readonly>"
        print email.message
        print "</textarea>"
        print "<br>"
        print "<input type='submit' class='inbox' name='back' formaction='trashcontroller.py' value='Back To Trash'/>"
        
        print "</form>"
        print "</body>"
        print "</html>"
        
# first time on this page
    def view(self,emails,userid):
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<head>"
        print "<link rel='stylesheet' type='text/css' href='./css/main.css'>"
        print "<title>Trash</title>"
        print "</head>"
        print "<html>"
        print "<body class='inbox'>"
        print "<br>"
        print "<div class='outter'>"
        print "<h1 class='inbox'>Trash</h1>"
        print "</div>"
        print "<br>"
        print "<p class='inbox'><a href='outboxcontroller.py'>Outbox</a> |  <a href='inboxcontroller.py'>Inbox</a> | <a href='trashcontroller.py'>Trash</a></p>"
        print "<br>"
        print "<form class='inbox' id='form' action='trashcontroller.py'  method='post'>"
        count=0;
        if emails is not None:
            for email in emails:
                print "<div class='message"+str(count)+"'> <input type='radio'  name='Num' value='"+email.Num+"' class='inputr'>"+"From: "+email.sender + "<br>"+"&emsp;&emsp;<b> Subject: " + email.subject +"</b></div>"
                if count is 0:
                    count=1
                else:
                    count=0
        print "<div class='input'>"
        print "<br>"
        print "   <input type='submit' class='inbox' id='Read_Email' name='readE' value='Read'/>"
        print "   <input  type='submit' class='inbox' id='Delete_Email' name='deleteE' value='Delete'/>"
        print "<br>"
        print "<br>"
        print "<br>"
        print "<input type='submit' class='inbox' id='LogOut' value='Logout' name='Logout'/>"
        print "</div>"
        print "</form>"
        print "</body>"
        print "</html>"

    def redirectLogin(self):
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<link rel='stylesheet' type='text/css' href='.css/main.css'>"
        print "<meta http-equiv='Refresh' content='0; url=logincontroller.py' />"
        print "</head>"
        print "<body>"
        print "<p> Please follow <a href='logincontroller.py'>this link</a></p>"
        print "</body>"
        print "</html>"

    def redirectDelete(self):
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<link rel='stylesheet' type='text/css' href='.css/main.css'>"
        print "<meta http-equiv='Refresh' content='0; url=trashcontroller.py' />"
        print "</head>"
        print "<body>"
        print "<p> Please follow <a href='trashcontroller.py'>this link</a></p>"
        print "</body>"
        print "</html>"
