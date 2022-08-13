from shelve import DbfilenameShelf
from flask import Flask,flash,render_template,redirect,session,request,flash
import os



app =Flask(__name__)

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
    if request.method == 'POST':
        
        
        return render_template('rent_book.html')
    else:
        print(title)

        return redirect('/')    

@app.route('/admin')
def admin():
    return render_template('admin.html')



if __name__ == '__main__':
    app.run(debug=True)