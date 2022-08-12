from flask import Flask,flash,render_template,redirect,session
from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bookrentals.db'
db = SQLAlchemy(app)



