from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager, AnonymousUserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:16122003@localhost/dbks?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "#@#$%%^%$#@#$$%^&**("
app.config["PAGE_SIZE"] = 6
pass_KS = "123"
db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Quan Ly Khach San", template_mode="bootstrap4")
my_login = LoginManager(app=app)
nhanvien = admin.name

class Anonymous(AnonymousUserMixin):
    def get_urole(self):
        return None

    @property
    def is_admin(self):
        return False

my_login.anonymous_user = Anonymous
app.jinja_env.globals.update(hasattr=hasattr)