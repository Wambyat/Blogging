from flask import Flask, redirect, url_for, request, render_template
import sqlite3
import os
from test_db import *

UP_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['UPLOAD_FOLDER'] = UP_FOLDER

login_check = 0
curr_user = "default"
curr_user_id = 0

#TODO make a profile page

#*################################################
#*           Login related functions             #
#*################################################


#!FINISHED
#######################################
#*              LOGIN PAGE            #

@app.route('/login/',methods = ['POST','GET'])
def login():

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

    error = "We have Over 10 Users!"
    print("Login here")

    global login_check
    global curr_user
    global curr_user_id

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
                curr_user_id = user_names.index(user)+1

                print("login changed")

                return redirect(url_for('feed'))
            
            else:

                error = 'Invalid Credentials. Try again'
                return render_template('login.html', error = error,logo_path = "..\\"+full_filename)
            
    else:

        return render_template('login.html', error = error,logo_path = "..\\"+full_filename)




#!FINISHED
#################################################
#*LOGOUT PAGE

@app.route('/logout/',methods = ['POST','GET'])
def logout():

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

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

    return render_template('logout.html', username = curr_user,logo_path = "..\\"+full_filename)




#!FINISHED
#################################################
#*PASSWORD RESET PAGE

@app.route('/passreset/',methods = ['POST','GET'])
def pass_reset():

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

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

    return render_template('passreset.html', error = error,logo_path = "..\\"+full_filename)




#! FINISHED
#*SIGN UP PAGE

@app.route('/signup/',methods = ['POST','GET'])
def signup():

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

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
            age = request.form['age']
            about = request.form['about']

            #Replacing all ' with '' in the sql query so that it can inset the ' into the text field.
            if "'" in about:

                about = about.replace("'","''")

        except:

            pass

        if user != "":

            if user not in user_names:

                try:

                    res = sql_query("user_info", "id")
                    res = [ i for j in res for i in j]
                    uid = max(res)+1

                    query = "INSERT INTO user_info VALUES ("+str(uid)+",'"+str(user)+"','"+str(password)+"')"

                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()

                    query = "INSERT INTO user_addi VALUES ("+str(uid)+","+str(age)+",'"+about+"')"
                    cursor.execute(query)
                    conn.commit()

                    conn.close()

                    login_check = 1
                    curr_user = user

                    return redirect(url_for('profile',name = user))
                
                except Exception as e:

                    print(e)
                    error = "Username already exists"
            
            else:
                    
                    error = "Username already exists"

    return render_template('signup.html',error = error,logo_path = "..\\"+full_filename)




#!FINISHED
#*REDIRECTOR FUNCTION (for login)

def redir_to_login():

    return redirect(url_for('login'))




#!FINISHED
#*REDIRECTOR FUNCTION (for logout)

def redir_to_logout():
    
    return redirect(url_for('logout',username = curr_user))

#################################################################################################

#*################################################
#*          Blog related functions               #
#*################################################


#################################################
#*               (testing page)                 #

@app.route('/test/',methods = ['POST','GET'])
def test():

    return render_template('profile.html')




#!FINISHED
#################################################
#*                 Main feed                    #

@app.route('/feed/',methods = ['POST','GET'])
def feed():

    if request.method == 'POST':

        print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOW")
        print(request.form['search'])

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

    if curr_user_id == 0:

        res = sql_query("user_info","id")
        res = [i for j in res for i in j]
        query1 = "SELECT * FROM blog_info WHERE uid IN "+str(tuple(res))
    
    else:

        #query to get blogs of users that the current user follows
        query1 = "SELECT * FROM blog_info WHERE uid IN (SELECT user_id FROM user_follow WHERE follower_id  = "+str(curr_user_id)+")"

    temp = sql_dir(query1)
    res=[]

    for i in temp:

        res.append([j for j in i])
        
    if res == []:

        res_content = ["You don't follow anyone."]
        res_titles = ["Please search for users!"]
        res_authors = ["- The team"]
        res_bid = [6]

    else:
        
        res_bid = [i[0] for i in res]
        res_titles=[i[1] for i in res]
        res_authors = [i[2] for i in res]
        res_content=[i[3] for i in res]        

        query = "SELECT name FROM user_info  WHERE id in "+str(tuple(res_authors))
        res_authors = sql_dir(query)
        res_authors= [j for i in res_authors for j in i]

    return render_template('feed.html', logo_path = "..\\"+full_filename, res1 = res_titles,res2=res_content, res3=res_authors, res4 = res_bid)




#!FINISHED
####################################
#*          SINGLE BLOG            #

@app.route('/blog/<int:blogID>/')
def blog(blogID):
    
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')

    query = "SELECT * FROM blog_info WHERE bid ="+str(blogID)
    res=sql_dir(query)
    res = [j for i in res for j in i]
    res1 = "admin"

    return render_template('blog.html',logo_path  = "..\\"+full_filename,id = res[0],titl = res[1], author = res1,dets = res[3]  )



#!FINISHED
#"home" page now just redirects to the feed

@app.route("/home/")
def home():

    return redirect(url_for('feed'))




#!FINISHED
#####################################
#*             profile page         #

@app.route('/profile/<name>/')
def profile(name):

    #Getting the user id using the username nad then using that to fetch the additional details.

    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')
    full_filename = url_for('static', filename='icon.jpg')

    name1 = name
    query = "SELECT id FROM user_info WHERE name LIKE '"+name+"'"

    res = sql_dir(query)
    res = [i for j in res for i in j]
    profile_user = res[0]
    query1 = "SELECT * FROM blog_info WHERE uid = "+str(profile_user)
    
    temp = sql_dir(query1)
    res=[]

    for i in temp:
        res.append([j for j in i])
        
    if res == []:

        res_content = ["You don't follow anyone."]
        res_titles = ["Please search for users!"]
        res_authors = ["- The team"]
        res_bid = [6]

    else:

        res_bid = [i[0] for i in res]
        res_titles=[i[1] for i in res]
        res_authors = [i[2] for i in res]
        res_content=[i[3] for i in res]        

        query = "SELECT name FROM user_info  WHERE id in "+str(tuple(res_authors))
        res_authors = sql_dir(query)
        res_authors= [j for i in res_authors for j in i]

    query = "SELECT * FROM user_addi WHERE uuid = "+str(profile_user)
    res = sql_dir(query)
    res = [i for j in res for i in j]

    about = res[2]
    age = res[1]

    return render_template('profile.html',logo_path = "..\\"+full_filename,username = name,about = about,age =age,res1 = res_titles ,res2=res_content,res3=res_authors,res4 = res_bid)




@app.route('/')
def home_page():

    if login_check == 0:

        return redir_to_login()

    else:

        return redirect(url_for('feed'))




@app.errorhandler(404)
def page_not_found(e):

    return "WOW 404"

if __name__ == '__main__':

    app.debug = True
    app.run()