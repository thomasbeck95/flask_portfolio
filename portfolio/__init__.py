from flask import Flask, render_template, flash, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from sqlalchemy.orm import declarative_base

app = Flask(__name__, static_folder="static")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'portfolio.db')
app.config["SECRET_KEY"] = 'can-you-guess-it'

db = SQLAlchemy(app)

Base = declarative_base()
Base.query = db.session.query_property()

import portfolio.routes