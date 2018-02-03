from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:letsbuild@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    #needs to list all blogs from database
    return render_template('base.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        return render_template('displaypost.html', blog = blog)

    else:

        return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    if request.method == "GET":
        return render_template('newpost.html')

    title = request.form['title']
    body = request.form['body']

    blog_instance = Blog(title, body)
    db.session.add(blog_instance)
    db.session.commit()

    return redirect('/displaypost?id={}'.format(blog_instance.id))
    




if __name__ == '__main__':
    app.run()