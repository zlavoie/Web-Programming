#!/usr/bin/env python
import Cookie



class LoginView:
    #redirect
    def redirect(self,cookie):
        print "Content-type: text/html"
        print cookie.output()
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<link rel='stylesheet' type='text/css' href='./css/main.css'>"
        print "<meta http-equiv='Refresh' content='0; url=inboxcontroller.py' />"
        print "</head>"
        print "<body>"
        print "<p>Please follow <a href='inboxcontroler.py'>this link</a>.</p>"
        print "</body>"
        print "</html>"
        print
        print

    def view(self):
        print "Content-type: text/html"
        print
        print "<!doctype html>"
        print "<head>"
        print "<title>Login Page</title>"
        print "<link rel='stylesheet' type='text/css' href='./css/main.css'>"
        print "</head>"
        print "<body class='login'>"
        print "<h1>Welcome To Zmail  Email System! </h1>"
        print "<h3 class='login'>Enter Your Information Below:</h3>"
        print "<form class='login2' id='form' method='post' action='logincontroller.py'>"
        print "   <p class='login2'>Username:   <input type='text' name='userid' /> </p>"
        print "   <p class='login2'>Password: <input type='password' name='password' /> </p>"
        print "   <input class='submit' type='submit' name='submit' value='Submit'/>"
        print "</form>"
        
        #Helpful User Message telling them their login/pass is not correct
       # if (not isValid(userid,password)and(not(str(userid)=="None") or not(str(password)=="None"))):    
        #    print "<p> Username/Password not in database</p>"

        print "<h3 class='login2'>New User? Sign Up Below: </h3>"
        print "<form class='login2' id='form2' method ='post' action='logincontroller.py'>"
        print "   <p class='login2'>New User ID:     <input type='text' name='useridNew' /></p>"
        print "   <p class='login2'>New Password: <input type='password' name='passwordNew'/></p>"
        print "   <input class='submit2' type='submit' name='submit2' value='Submit' />"
        print "</form>"
        print "</bod1y>"
        print "</html>"
