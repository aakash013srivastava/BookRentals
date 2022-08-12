from flask import Flask,flash,render_template,redirect,session
from flask_sqlalchemy import SQLAlchemy
import os

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bookrentals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


BOOK_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = BOOK_FOLDER

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    author = db.Column(db.String(80),nullable=False)
    year = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<Book %s --by:%s>'.format(self.title,self.author)


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

@app.route('/rent_book')
def rent_book():
    return render_template('rent_book.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')



if __name__ == '__main__':
    app.run(debug=True)