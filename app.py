from shelve import DbfilenameShelf
from flask import Flask,flash,render_template,redirect,session,request,flash
from werkzeug.utils import secure_filename

import os


app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    imageList = os.listdir('static/images')
    images = ['static/images/' + image for image in imageList]
    print(images)
    return render_template("index.html", images=images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rent_book/<title>',methods=['GET','POST'])
def rent_book(title):


    print(title)
    f = open('request.txt','a')
    f.write("email:"+"aakash@gmail.com"+",title:"+title+"\n")
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