 
import cgi
import cgitb
import sys
import Cookie


#
# isValid()
#
def isValid(userid, password):
    with open('UserIdPass.txt', 'r') as file:
        # read the file into lines
        lines = file.readlines() 

        # iterate through lines, splitting each line into strings
        for line in lines:
            strings = iter(line.split())

            # process each string pair, return True if match
            # otherwise when end of file reached, drop to return False
            while True:
                try:
                    fileUserId = strings.next()
                    filePassword = strings.next()

                    # we have a match
                    if (userid == fileUserId) and (password == filePassword):
                        return True

                except StopIteration:
                    break
    return False

#
# Main Program
#


def main():
    form = cgi.FieldStorage() 
    userid   = form.getvalue('userid')
    password = form.getvalue('password')

    useridNew = form.getvalue('useridNew')
    passwordNew = form.getvalue('passwordNew')
    space = " "
    
    if (not(str(useridNew)==str("None")) and not(str(passwordNew)=="None")):
        if not(isValid(useridNew,passwordNew)):
            f=open("UserIdPass.txt","a")
            f.write(str(useridNew))
            f.write(str(space))
            f.write(str(passwordNew))
            f.write("\n")
            f.close()
            #write the new user a file to hold their email information
            f=open((str(useridNew)+".txt"),"w+")
            #write the new user a file to hold their sent messages
            f=open((str(useridNew)+".txt"),"w+")
            f.close()

            
    if isValid(userid,password):
        cookie = Cookie.SimpleCookie()
        cookie['userid']=userid
        
        print "Content-type: text/html"
        print cookie.output()
        print
        print "<!doctype html>"
        print "<html>"
        print "<head>"
        print "<meta http-equiv='Refresh' content='0; url=inbox.py' />"
        print "<link rel='stylesheet' type='text/css' href='./css/main.css'>"
        print "</head>"
        print "<body>"
        print "<p>Please follow <a href='inbox.py'>this link</a>.</p>"
        print "</body>"
        print "</html>"
        print
        print

    else:
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
        print "<form id='form' method='post' action='login.py'>"
        print "   <p>Username:   <input type='text' name='userid' /> </p>"
        print "   <p>Password: <input type='password' name='password' /> </p>"
        print "   <input type='submit' name='submit' value='submit'/>"
        print "</form>"
        if (not isValid(userid,password)and(not(str(userid)=="None") or not(str(password)=="None"))):    
            print "<p> Username/Password not in database</p>"
        print "<h3 class='login'>New User? Sign Up Below: </h3>"
        print "<form id='form2' method ='post' action='login.py'>"
        print "   <p>New User ID: <input type='text' name='useridNew' /></p>"
        print "   <p>New Password: <input type='password' name='passwordNew'/></p>"
        print "   <input type='submit' name='submit2' value='submit' />"
        print "</form>"
        print "</bod1y>"
        print "</html>"
main()
