from flask import Flask, redirect, url_for, request, render_template
import sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
login_check = 0
curr_user = ""
#This function will take table name and required column as input. It will return a list of all values in that column.

#TODO logout page, password reset and sign up logic and final htmls

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

@app.route('/login/',methods = ['POST','GET'])
def login():
    error = "We have Over 10 Users!"
    print("Login here")
    global login_check
    global curr_user
    if login_check == 1:
        return render_template('logout.html', username = curr_user)

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
        

        print("posting")
        user = request.form['username']
        password = request.form['password']
        


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


@app.route('/passreset/',methods = ['POST','GET'])
def pass_reset():
    return render_template('passreset.html')

@app.route('/signup/',methods = ['POST','GET'])
def signup():
    return render_template('signup.html')

def redir_to_login():
    print("here OOOOOOOOOOOOOGGGGGGGGGGGGGAAAAAAAAAAAAAAAAAAAAA") #Changing this print statement fixed the code for some reason?
    return redirect(url_for('login'))
    

@app.route('/blog/<int:blogID>/')
def blog_disp(blogID):
    if login_check == 0:
        redir_to_login()
    return "This is blog " + str(blogID)

@app.route("/home/<int:var1>/")
def home(var1):
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