from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = b']UB\xbb\xfa\xec\xa2\x0e\x1a\xceO\xcfE3-\x11'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://[usuario]:[senha]@localhost/[database]"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from todo_app.routes import *
