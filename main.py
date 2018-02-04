from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:letsshare@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secretkey'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.String(15), db.ForeignKey('user.username'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(600))
    blogs = db.relationship('Blog', backref ='owner')

@app.before_request
def authenticate():
    public = ['blog', 'signup','login','index']
    if request.endpoint not in public and 'username' not in session:
        session['authenticate']='Please login first.'
        verify = session.get('authenticate')
        return render_template('login.html', top = 'Error', authenticate = verify)

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordverify = request.form['passwordverify']
        user_object = User.query.filter_by(username = username).first()
        
        if username == '' or password == '' or passwordverify == '':
            return render_template('signup.html', invalid = 'Username and/or Password is missing.',)
        if len(username) < 3:
            return render_template('signup.html', invalid = 'Please make your username longer',)
        if username.isalnum() == False:
            return render_template('signup.html', invalid = 'unauthorized Character')
        if user_object != None:
            return render_template('signup.html', invalid = 'Username is taken.')
        if len(password) < 3:
            return render_template('signup.html', shortPW = 'Please make your password longer.')
        if password != passwordverify:
            return render_template('signup.html', invalid = "Password doesn't match")

        
        userObject = User(username, password,)
        database.session.add(userObject)
        database.session.commit()
        session['username'] = username
        return redirect('/newpost')

    if 'authenticate'in session:  
        del session['authenticate']
    return render_template('signup.html', top = 'Registration')


app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        #limit the number of attempt with session['attempt'] = 10
        username = request.form['username']
        password = request.form['password']
        user_object = User.query.filter_by(username = username).first()
        if user_object == None:
            return render_template('login.html', top = 'Login', user = 'Username not found.')
        if user_object.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('login.html', top = 'Login', wrong = 'Incorrect Password.',username = username)

    return render_template('login.html', top = 'Login')

@app.route('/logout', methods = ['GET'])
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    blogs = Blog.query.all() 
    #needs to list all blogs from database
    return render_template('index.html', blog=blogs)


@app.route('/user')
def user():
    users = User.query.all()
    return render_template('userindex.html', user=users)

@app.route('/displaypost')
def show():
    displayid = request.args.get("blogid")
    blogs = Blog.query.get(displayid)
    return render_template('displaypost.html',blog = blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    if request.method == "GET":
        return render_template('newpost.html')

    title = request.form['title']
    body = request.form['body']
    id = request.form['owner_id']

    if not (title or body):
        return render_template('newpost.html', title = 'Please add a title', body = 'Please share your thoughts') 

    blog_instance = Blog(title, body, id)
    db.session.add(blog_instance)
    db.session.commit()

    return redirect("/")
    

if __name__ == '__main__':
    app.run()