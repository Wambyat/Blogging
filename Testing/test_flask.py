from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)
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

def redir_to_login():
    print("here")
    

@app.route('/blog/<int:blogID>/')
def blog_disp(blogID):
    if login_check == 0:
        redir_to_login()
    return "This is blog " + str(blogID)

@app.route("/home/<int:var1>/")
def home(var1):
    if login_check == 0:
        redir_to_login()
    if var1 > 50:
        return redirect(url_for('blog_disp',blogID = var1))
    else:
        return "Wow this works?"

@app.route('/profile/<name>/')
def profile(name):
    if login_check == 0:
        return redirect(url_for('login'))
    return "Hello " + name + str(login_check)

@app.route('/')
def home_page():
    if login_check == 0:
        redir_to_login()
    else:
        return " This is home" 

if __name__ == '__main__':
    app.debug = True
    app.run()