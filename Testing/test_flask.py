from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
login_check = 0


@app.route('/login/',methods = ['POST','GET'])
def login():
    error = None
    print("Login here")
    global login_check
    if request.method == 'POST':
        
        print("posting")
        user = request.form['username']
        password = request.form['password']
        
        if user == "admin" and password == "admin":
            #Login success
            login_check = 1
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