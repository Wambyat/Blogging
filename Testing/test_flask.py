from flask import Flask, redirect, url_for, request, render_template

import sqlite3
import os
from test_db import *

UP_FOLDER = os.path.join('static', 'uploads')
ALLOWED_FILES = ('png', 'jpg', 'jpeg', 'gif')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['UPLOAD_FOLDER'] = UP_FOLDER

full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'icon.jpg')
path = os.path.join(app.config['UPLOAD_FOLDER'], 'p1.png')

login_check = 0
curr_user = "default"
curr_user_id = 0

#sql functions are imported from test.db

#*################################################
#*           Login related functions             #
#*################################################


#!FINISHED
#######################################
#*              LOGIN PAGE            #

@app.route('/login/',methods = ['POST','GET'])
def login():

    global full_filename
    global path
    print(full_filename)
    print(path)
    
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

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

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
                return render_template('login.html', error = error,logo_path = "..\\"+full_filename,img_path = path)
            
    else:

        return render_template('login.html', error = error,logo_path = "..\\"+full_filename,img_path = path)




#!FINISHED
#################################################
#*LOGOUT PAGE

@app.route('/logout/',methods = ['POST','GET'])
def logout():

    global full_filename

    global login_check
    global curr_user

    print("Pain is gay")

    if login_check == 0:

        return redir_to_login()

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

        if "logout" in request.form:
                
            login_check = 0
            curr_user = ""

            return redirect(url_for('login'))

    return render_template('logout.html', username = curr_user,logo_path = "..\\"+full_filename,currname = curr_user)




#!FINISHED
#################################################
#*PASSWORD RESET PAGE

@app.route('/passreset/',methods = ['POST','GET'])
def pass_reset():

    global full_filename

    if login_check == 1:

        print("ogga")
        return redir_to_logout()

    error = "Please enter the new password"
    username = ""

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

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

    global full_filename

    error = "Enter your desired username and password"
    print("Sign up here")

    global login_check
    global curr_user

    print("Login check" +  str(login_check))

    if login_check == 1:

        return redir_to_logout()

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

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


#?These are kinda useless but they remain cuz i've run out of time

#!FINISHED
#*REDIRECTOR FUNCTION (for login)

def redir_to_login():

    return redirect(url_for('login'))


#!FINISHED
#*REDIRECTOR FUNCTION (for logout)

def redir_to_logout():
    
    return redirect(url_for('logout'))



#################################################################################################
#*################################################
#*          Blog related functions               #
#*################################################




##################################################
#*                   New Blog                    #
@app.route('/newblog/',methods = ['POST','GET'])
def newblog():

    global full_filename
    global login_check

    blog_id = 0

    if login_check == 0:

        print("ogga")
        return redir_to_login()

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

        
        
        try:
            print("here?")
            title = request.form['title']
            content = request.form['content']

            if "'" in title:
                
                title = title.replace("'","''")
            if "'" in content:
                
                content = content.replace("'","''")
            
            blog_id = new_blog(title,content,curr_user_id)

            ur = "http://127.0.0.1:5000/blog/"+str(blog_id)
            
        except Exception as e:
            print(e)

        if "image" not in request.files:

            print("No image found")
            
        
        else:

            file = request.files['image']
            a = "\\bb"+str(blog_id)+".png"
            path = "C:\School Files\Lab_Records\IIT_Stuff\MAD1_Project\MAD-1-Project\Testing\static\\uploads"+a
            file.save(path)
            print("Image saved")
            return redirect(ur)

    return render_template('newblog.html',logo_path = "..\\"+full_filename,currname = curr_user)

#!FINISHED
#################################################
#*                 Main feed                    #

@app.route('/feed/',methods = ['POST','GET'])
def feed():

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

    global full_filename
    global login_check

    logi = "a" if login_check == 0 else "b"

    if curr_user_id == 0:

        res = sql_query("user_info","id")
        res = [i for j in res for i in j]
        query1 = "SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE uid IN "+str(tuple(res))
    
    else:

        #query to get blogs of users that the current user follows
        query1 = "SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE uid IN (SELECT user_id FROM user_follow WHERE follower_id  = "+str(curr_user_id)+")"

    temp = sql_dir(query1)
    res=[]

    for i in temp:

        res.append([j for j in i])
        
    if res == []:

        res_content = ["You don't follow anyone."]
        res_titles = ["Please search for users!"]
        res_author = ["- The team"]
        res_bid = [6]

    else:
        
        res_bid = [i[0] for i in res]
        res_titles = [i[1] for i in res]
        res_content = [i[2] for i in res]
        res_author = [i[3] for i in res]

    path ="C:\School Files\Lab_Records\IIT_Stuff\MAD1_Project\MAD-1-Project\Testing\static\\uploads\icon.jpg"

    return render_template('feed.html', logo_path = path,logi = logi, res1 = res_titles,res2=res_content, res3=res_author, res4 = res_bid,currname = curr_user)



#TODO Add follow unfollow and like dislike and edit
#!FINISHED
####################################
#*          SINGLE BLOG            #

@app.route('/blog/<int:blogID>/',methods = ['POST','GET'])
def blog(blogID):
    
    global full_filename

    if request.method == 'POST':
        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

        if "like" in request.form:
            
            like_blog(blogID,curr_user_id)
            return redirect(url_for('blog',blogID = blogID))

        if "unlike" in request.form:
            
            like_blog(blogID,curr_user_id)
            return redirect(url_for('blog',blogID = blogID))

        if "delete" in request.form:
            
            print("This works?????????????????????")
            delete_blog(blogID)
            ur = "http://127.0.0.1:5000/profile/"+str(curr_user)
            return redirect(ur)


        if "title" in request.form:
            
            title = request.form['title']
            content = request.form['conte']

            if "'" in title:
                    
                title = title.replace("'","''")
            if "'" in content:
                    
                content = content.replace("'","''")

            update_blog(blogID,title,content)
            return redirect(url_for('blog',blogID = blogID))

    blog_list = sql_query("blog_info","bid")
    blog_list = [i for j in blog_list for i in j]

    if blogID not in blog_list:
        blogID = 0

    edi = same_user(blogID,curr_user_id)

    print(edi)

    query = "SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE bid ="+str(blogID)
    res=sql_dir(query)
    res = [j for i in res for j in i]
    res1 = "admin"

    path ="C:\School Files\Lab_Records\IIT_Stuff\MAD1_Project\MAD-1-Project\Testing\static\\uploads\icon.jpg"

    no_of_likes = get_likes(blogID)

    return render_template('blog.html',logo_path = "..\\"+full_filename,img_path = path,id = res[0],titl = res[1], author = res[3],conte = res[2],edi = edi,currname = curr_user,no_of_likes = no_of_likes) 



#!FINISHED
#"home" page now just redirects to the feed

@app.route("/home/")
def home():

    return redirect(url_for('feed'))



@app.route("/fols/<name>/")
def fols(name):

    #need to give logi,currname,fol,fing
    logi = "a" if login_check == 0 else "b"
    currname = curr_user

    uid = get_user_id(name)

    fol =get_following(uid)
    fing = get_followers(uid)

    if len(fol) == 1:

        query = "SELECT name FROM user_info WHERE id = "+str(fol[0])

    else:

        query = "SELECT name FROM user_info WHERE id in "+str(tuple(fol))

    fol = sql_dir(query)
    fol = [i[0] for i in fol]

    if len(fing) == 1:

        query = "SELECT name FROM user_info WHERE id = "+str(fing[0])
    
    else:
        query = "SELECT name FROM user_info WHERE id in "+str(tuple(fing))

    fing = sql_dir(query)
    fing = [i[0] for i in fing]

    return render_template('fol.html',logi = logi,currname = currname,fol = fol,fing = fing)    




#TODO Add follower and following and edit
#!FINISHED
#####################################
#*             profile page         #

@app.route('/profile/<name>/',methods = ['POST','GET'])
def profile(name):

    #Getting the user id using the username nad then using that to fetch the additional details.

    global full_filename
    global login_check

    if login_check == 0:
            
        return redirect(url_for('login'))

    if name == "default":

        name = "John"

    if request.method == 'POST':

        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

        if "uname_up" in request.form:
                
            uname = request.form['uname']
            update_user_info(curr_user_id,uname)
            return redirect(url_for('profile',name = uname))
        
        if "about_up" in request.form:
                
            about = request.form['about']
            age = request.form['age']
            update_user_addi(curr_user_id,age,about)
            return redirect(url_for('profile',name = name))
        
        if "delete" in request.form:
                
            delete_user(curr_user_id)
            
            login_check = 0
            return redirect(url_for('login'))
        
        if "follow" in request.form:

            uid = get_user_id(name)        
            follow_user(uid,curr_user_id)
            return redirect(url_for('profile',name = name))
        
        if "unfollow" in request.form:

            uid = get_user_id(name)        
            follow_user(uid,curr_user_id)
            return redirect(url_for('profile',name = name))

    logi = "a" if login_check == 0 else "b"

    query = "SELECT id FROM user_info WHERE name = '"+name+"'"

    res = sql_dir(query)
    res = [i for j in res for i in j]

    profile_user = res[0]


    query1 = "SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE uid ="+str(profile_user)

    temp = sql_dir(query1)
    res=[]

    for i in temp:
        res.append([j for j in i])


    if res == []:

        res_content = ["You don't have any posts."]
        res_titles = ["Make a blog :)"]
        res_author = ["- The team"]
        res_bid = [0]

    else:
            
        res_bid = [i[0] for i in res]
        res_titles = [i[1] for i in res]
        res_content = [i[2] for i in res]
        res_author = [i[3] for i in res]

    query = "SELECT * FROM user_addi WHERE uuid = "+str(profile_user)
    res = sql_dir(query)
    res = [i for j in res for i in j]

    about = res[2]
    age = res[1]

    edi = "a" if name == curr_user else "b"

    uid = get_user_id(name)

    fol = get_followers(uid)
    print(fol)

    if curr_user_id in fol:

        fol ="f"
    else :
        fol = "n"

    no_of_blogs = get_blogs(uid)

    return render_template('profile.html',logo_path = "..\\"+full_filename,logi = logi,username = name,about = about,age =age,res1 = res_titles ,res2=res_content,res3=res_author,res4 = res_bid,currname = curr_user,edi = edi,fol =fol,no_of_blogs = no_of_blogs)


#!FINISHED
#####################################
#*             search page          #
@app.route("/search/<term>/",methods = ['POST','GET'])
def search(term):

    if request.method == 'POST':
            
        if "search" in request.form:

            term = request.form['search']
            return redirect(url_for('search',term = term))

    res = search_func(term)

    # res1 = res_titles,res2=res_content, res3=res_author, res4 = res_bid

    res_b = res["blog"][:]
    res_u = res["user"][:]

    if res_b == []:
        res_titles = ["No blogs found"]
        res_content = ["Please try a different name!"]
        res_author = ["- The team"]
        res_bid = [0]
    else:

        res_bid = [i[0] for i in res_b]
        res_titles = [i[1] for i in res_b]
        res_content = [i[2] for i in res_b]
        res_author = [i[3] for i in res_b]

    if res_u == []:

        res11 = ["No users found"]
        res22 = ["Please try a different name!"]
    
    else:
            
        res11 = [i[0] for i in res_u]
        res22 = [i[1] for i in res_u]

    return render_template('search.html',res1 = res_titles ,res2=res_content,res3=res_author,res4 = res_bid,res11 = res11,res22 = res22,currname = curr_user)



@app.route('/')
def home_page():

    if login_check == 0:

        return redir_to_login()

    else:

        return redirect(url_for('feed'))




@app.errorhandler(404)
def page_not_found(e):

    return render_template('error.html'), {"Refresh": "3; url=http://127.0.0.1:5000/home/"}

if __name__ == '__main__':

    app.debug = True
    app.run()