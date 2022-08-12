from flask import Flask,flash,render_template,redirect,session,request
import os
from flask_mysqldb import MySQL,MySQLdb
# from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bookrentals.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)


# BOOK_FOLDER = os.path.join('static', 'images')
# app.config['UPLOAD_FOLDER'] = BOOK_FOLDER

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), unique=True, nullable=False)
#     isbn = db.Column(db.Integer, unique=True, nullable=False)
#     author = db.Column(db.String(80),nullable=False)
#     year = db.Column(db.Integer,nullable=False)

#     def __repr__(self):
#         return '<Book %s --by:%s>'.format(self.title,self.author)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'BookRentals'

mysql = MySQL(app)

app.secret_key= 'mysecretkey'

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

@app.route('/rent_book',methods=['GET','POST'])
def rent_book():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(
                'SELECT * FROM Books WHERE isbn = % s', (request.form['isbn']))
            account = cursor.fetchone()
        except:
            print("Error")
        else:
            if account == '0' or account == 0:
                try:
                    cursor.execute(
                        'INSERT into FROM Books(title,isbn,author,year) values(%s,%s,%s,%s)',
                        (request.form['title'],request.form['isbn'],request.form['author'],request.form['year']))
                except:
                    print("Error while creating book record")
                    flash("Could not add book to database")
        finally:
            cursor.close()
        return render_template('rent_book.html')
    return render_template('rent_book.html')    

@app.route('/admin')
def admin():
    return render_template('admin.html')



if __name__ == '__main__':
    app.run(debug=True)