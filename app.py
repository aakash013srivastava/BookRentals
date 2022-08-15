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
    if len(lines)>0:
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
    if 'email' in session:
        return render_template("index.html", images=images,email=session['email'])
    return render_template("index.html", images=images,email=None)

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
            flash('User registered !!!')
        else:
            flash('User Already registered')
        return redirect('/login')
    return render_template('register.html')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        with open('Users.txt','r') as f:
            flag = False
            lines = f.readlines()
            if len(lines)>0:
                print(lines)
                for line in lines:
                    email = (line.split(',')[0]).split(':')[1].strip()
                    password = (line.split(',')[1]).split(':')[1].strip()
                    print((password == request.form['exampleInputPassword1']))
                    print(len(password))
                    if request.form['exampleInputEmail1'] == email and request.form['exampleInputPassword1'] == password:
                        session['email'] = email
                        flash('You have successfully logged in')
                        return redirect('/')
                    elif request.form['exampleInputEmail1'] == email and request.form['exampleInputPassword1'] != password:
                        flash('Wrong Email/Password combination')
                        return redirect('/login')                    
                flash('User does not exist')
                return redirect('/register')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    flash('You have successfully Logged Out !!!')
    return redirect('/')


@app.route('/rent_book/<title>',methods=['GET','POST'])
def rent_book(title):


    print(title)
    f = open('request.txt','a')
    f.write("email:"+session['email']+",fileName:"+title+"\n")
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

    f= open('request.txt','r')
    file = f.readlines()
    f.close()
    return render_template('admin.html',email=session['email'] if 'email' in session else None,requests=file)

@app.route('/serve_request/<requested>')
def serve(requested):
    f = open('request.txt','r')
    lines = f.readlines()
    print(lines)
    print(requested)
    f.close()
    for line in range(0,len(lines)):
        if lines[line].strip() == requested:
            lines[line] = ''

    f = open('request.txt','w')
    f.write("".join(lines))
    f.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)