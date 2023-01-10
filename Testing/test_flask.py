from flask import Flask, redirect, url_for, request, render_template
import sqlite3

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_check = 0
curr_user = "default"

#TODO accept username and password through a function

#################################################
#*             SQL functions                    #
#################################################
#This function will take table name and required column as input. It will return a list of all values in that column.
def sql_query(tbl , col):
    
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        print("\nConnecting to database\n")

        query = "SELECT "+str(col)+" FROM "+str(tbl)
        cursor.execute(query)
        result = cursor.fetchall()
        
    except Exception as e:

        result = "Error"

    finally:

        conn.commit()
        conn.close()
        print("\nConnection closed\n")
        return result
#####################################################################################################################




#################################################
#*          Login related functions             #
#################################################


#*LOGIN PAGE

@app.route('/login/',methods = ['POST','GET'])
def login():

    error = "We have Over 10 Users!"
    print("Login here")

    global login_check
    global curr_user

    print("Login check" +  str(login_check))

    if login_check == 1:

        print("ogga")
        return redir_to_logout()

    if request.method == 'POST':

        user_names = sql_query("user_info","name")

        if type("abc") == type(user_names):
            print(user_names)

        else:

            #This formats the result into a list of strings
            user_names = [j for i in user_names for j in i]
        
        
        passwords = sql_query("user_info","password")

        if type("abc") == type(passwords):
            print(passwords)

        else:
            #This formats the result into a list of strings
            passwords = [j for i in passwords for j in i]
        
        user  = ""
        password = ""

        print("posting")
        try:
            user = request.form['username']
            password = request.form['password']
        except:
            pass

        if user != "":

            if user in user_names and password == passwords[user_names.index(user)]:

                #Login success
                login_check = 1
                curr_user = user
                print("login changed")

                return redirect(url_for('profile',name = user))
            
            else:

                error = 'Invalid Credentials. Try again'

                return render_template('login.html', error = error)
            
    else:

        return render_template('login.html', error = error)

#################################################

#*LOGOUT PAGE

@app.route('/logout/',methods = ['POST','GET'])
def logout():

    global login_check
    global curr_user

    print("Pain is gay")

    if login_check == 0:

        return redir_to_login()

    if request.method == 'POST':

        if "logout" in request.form:
                
            login_check = 0
            curr_user = ""

            return redirect(url_for('login'))

    return render_template('logout.html', username = curr_user)


#################################################

#*PASSWORD RESET PAGE

@app.route('/passreset/',methods = ['POST','GET'])
def pass_reset():

    error = "Please enter the new password"
    username = ""

    if request.method == 'POST':

        error = "Please enter the new password"
        username = ""

        try:

            username = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']

        except:

            pass

        if username != "":        

            if password == password2:

                try:

                    query = "UPDATE user_info SET password = '"+str(password)+"' WHERE name = '"+str(username)+"'"
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()
                    conn.close()

                    print("Password changed")
                    error = "Password changed successfully"


                except Exception as e:

                    error = "Please enter credentials correctly"

            else:

                error = "Passwords do not match"

    return render_template('passreset.html', error = error)


#*SIGN UP PAGE

@app.route('/signup/',methods = ['POST','GET'])
def signup():

    error = "Enter your desired username and password"
    print("Sign up here")

    global login_check
    global curr_user

    print("Login check" +  str(login_check))

    if login_check == 1:

        return redir_to_logout()

    if request.method == 'POST':

        user_names = sql_query("user_info","name")

        if type("abc") == type(user_names):
            print(user_names)

        else:

            #This formats the result into a list of strings
            user_names = [j for i in user_names for j in i]
        
        
        passwords = sql_query("user_info","password")

        if type("abc") == type(passwords):
            print(passwords)

        else:
            #This formats the result into a list of strings
            passwords = [j for i in passwords for j in i]
        
        user  = ""
        password = ""

        print("posting")

        try:

            user = request.form['username']
            password = request.form['password']

        except:

            pass

        if user != "":

            if user not in user_names:

                try:

                    query = "INSERT INTO user_info (name,password) VALUES ('"+str(user)+"','"+str(password)+"')"
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()
                    conn.close()

                    login_check = 1
                    curr_user = user

                    return redirect(url_for('profile',name = user))
                
                except:
                        
                    error = "Username already exists"
            
            else:
                    
                    error = "Username already exists"

    return render_template('signup.html',error = error)


#*REDIRECTOR FUNCTION (for login)

def redir_to_login():

    return redirect(url_for('login'))
    

#*REDIRECTOR FUNCTION (for logout)

def redir_to_logout():
    
    return redirect(url_for('logout',username = curr_user))

######################################################################################################################

#################################################
#          Blog related functions               #
#################################################

#################################################
#*                    BLOG PAGE                 #
#################################################
@app.route('/testblog/',methods = ['POST','GET'])
def blog_test():
    return render_template('blog.html')


@app.route('/blog/<int:blogID>/')
def blog_disp(blogID):

    if login_check == 0:

        redir_to_login()

    return "This is blog " + str(blogID)

@app.route("/home/")
def home():
    var1= 55

    if login_check == 0:

        return redir_to_login()

    elif var1 > 50:

        return redirect(url_for('blog_disp',blogID = var1))

    else:

        return "Wow this works?"+str(login_check)

@app.route('/profile/<name>/')
def profile(name):

    if login_check == 0:

        return redirect(url_for('login'))

    return "Hello " + name + str(login_check)

@app.route('/')
def home_page():

    if login_check == 0:

        return redir_to_login()

    else:

        return " This is home" 

@app.errorhandler(404)
def page_not_found(e):

    return "WOW 404"

if __name__ == '__main__':

    app.debug = True
    app.run()