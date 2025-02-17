from flask import Flask,render_template,request,session,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import json
from flask_mail import Mail,Message
import os
from werkzeug.utils import secure_filename
import math


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('Mail_Username') #Featching the email from Envirnoment Variable
app.config['MAIL_PASSWORD'] = os.getenv('Mail_Pswd') # Featching the app password from Envirnoment Variable
app.config['MAIL_DEFAULT_SENDER'] = ('Hari Kishore', os.getenv('Mail_Username'))
mail = Mail(app)

#reading the config file
with open('config.json') as c:
    params = json.load(c)["params"]

if (params["localhost"]):
    # configure the SQL database
    app.config["SQLALCHEMY_DATABASE_URI"] =  params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] =  params["params"]["prod_uri"]

#for setting the location of the uploader
app.config['UPLOAD_FOLDER'] = params['upload_location']
#database connection
db = SQLAlchemy(app)    

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    tagline = db.Column(db.String(50),nullable = False)
    subtitle = db.Column(db.String(50),nullable = False)
    slug = db.Column(db.String(25),nullable = False)
    content = db.Column(db.String(200),nullable = False)
    date = db.Column(db.String(25),nullable = True)
    name = db.Column(db.String(25),nullable = False)
   
class Contacts(db.Model):
    """sno,name,ph_num,msg,date,email"""
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable = False)
    ph_num = db.Column(db.String(13),nullable = False)
    msg = db.Column(db.String(50),nullable = False)
    date = db.Column(db.String(25),nullable = True)
    email = db.Column(db.String(30),nullable = False)

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/params["nopost"])
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*(int(params['nopost'])) : (page-1)*int(params['nopost']) + (int(params['nopost']))]
    if(page == 1 and last == 1):
        prev = "#"
        next = "#" 

    elif(page == 1):
        prev = "#"
        next = "/?page=" + str(page+1)

    elif (page == last):
        prev = "/?page="+str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)
    
    return render_template("index.html",posts=posts,params = params, prev = prev, next = next)

@app.route("/dashboard", methods=['GET', 'POST'])

def dashboard():
    if (('user' in session) and (session['user'] == params['admin_user'])):
            posts = Posts.query.all()
            return render_template('dashboard.html',params = params, posts = posts)
    if request.method=="POST":
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username== params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", params = params, posts = posts)
    else:
        return render_template("login.html",params = params)
        
    return render_template("login.html", params=params)

@app.route("/uploader",methods = ["GET","POST"])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method == "POST"):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))) #joins the uploaded folder with name of any file
            return("Upload success!")


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        # If the request method is POST, handle the form submission
        if request.method == 'POST':
            name = request.form.get('name')
            title = request.form.get('title')
            tline = request.form.get('tline')
            subtitle = request.form.get('stitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            date = datetime.now()

            if sno == '0':
                # If sno is '0', this means a new post is being created
                post = Posts(name=name, title=title, tagline=tline, subtitle=subtitle,
                             slug=slug, content=content, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.tagline = tline
                post.subtitle = subtitle
                post.slug = slug
                post.content = content
                post.name = name
                post.date = date
                
                db.session.commit()
                return redirect('/edit/sno')

    post = Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html', params = params, post = post, sno = sno)

    #for api request
    @app.route("/api/posts", methods=["GET"])
    def get_posts():
    posts = Posts.query.all()
    posts_data = [
        {
            "sno": post.sno,
            "title": post.title,
            "tagline": post.tagline,
            "subtitle": post.subtitle,
            "slug": post.slug,
            "content": post.content,
            "date": post.date,
            "name": post.name
        }
        for post in posts
    ]
    return jsonify(posts_data)

@app.route("/about")
def about():
    return render_template("about.html")
    
# post request
@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    # Fetch the post matching the slug
    post = Posts.query.filter_by(slug=post_slug).first()    
    # Handle the case where no post is found
    if post is None:
        return "Post not found", 404  
    # Render the template with the post data
    return render_template("post.html", post=post)

@app.route("/contact",methods = ['GET','POST'])
def contact():
    if(request.method == 'POST'):
        #entry
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        #sno,name,ph_num,msg,date,email
        entry = Contacts(name=name , ph_num=phone , msg=message , date = datetime.now() , email=email )
        db.session.add(entry)
        db.session.commit()
        # email message
        msg = Message(subject="Mail from webpage ",
                      recipients=['abcperson@gmail.com'],
                      body=f'This message was sent by {name}, Phone no. - {phone} \n Message : {message}',
                      date= 144)
        try:
            mail.send(msg)
        except Exception as e:
            print(f'failed to send email:{str(e)}')

    return render_template("contact.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
