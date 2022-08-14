from shelve import DbfilenameShelf
from flask import Flask,flash,render_template,redirect,session,request,flash
from werkzeug.utils import secure_filename

import os


app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECRET_KEY'] = '12345'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_registration():
    f = open('Users.txt','r')
    flag = False
    lines = f.readlines()
    for line in lines:
        email = (line.split(',')[0]).split(':')[1]
        password = (line.split(',')[1]).split(':')[1]
        if request.form['exampleInputEmail1'] == email:
            return True
    f.close()
    return False
        


@app.route('/')
def index():
    imageList = os.listdir('static/images')
    images = ['static/images/' + image for image in imageList]
    print(images)
    return render_template("index.html", images=images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        isRegistered = check_registration()
        if not isRegistered:
            f = open('Users.txt','a')
            f.write("email:"+request.form['exampleInputEmail1']+",password:"+request.form['exampleInputPassword1']+"\n")
            f.close()
            
        else:
            flash('User Already registered')
        return redirect('/login')
    return render_template('register.html')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        f1 = open('Users.txt','a')
        if os.stat('Users.txt').st_size != 0:
            ls = f1.readlines()
            if len(ls):
                for line in ls:
                    l1=line.split(",")
                    for l in l1:
                        l2=l1.split(':')
                        print(l2)
                    
        f1.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/rent_book/<title>',methods=['GET','POST'])
def rent_book(title):


    print(title)
    f = open('request.txt','a')
    f.write("email:"+"aakash@gmail.com"+",fileName:"+title+"\n")
    f.close()
    return redirect('/')    

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        img = request.files['formFile']
        if img.filename != '':
             
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img.filename)))
        f = open('books.txt','a')
        f.write("title:"+request.form['title']+",isbn:"+request.form['isbn']+",author:"+request.form['author']+",year:"+request.form['year']+",fileName:"+request.files['formFile'].filename+"\n")
        f.close()
        flash('Book was added to DB')
        return redirect('/')
    return render_template('admin.html')



if __name__ == '__main__':
    app.run(debug=True)