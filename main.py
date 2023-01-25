from flask import Flask, render_template, flash, redirect, url_for, request
from config import host, port
from db import db_get_user, NoSuchEmailError
from db import db_get_all_users
from db import db_add_user
from db import db_get_user_by_email
from flask_login import LoginManager, login_user, current_user
from forms import RegistrationForm, LoginForm
from models import User
import os

SECRET_KEY = os.urandom(32)

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)
app.config['SECRET_KEY'] = SECRET_KEY


@login_manager.user_loader
def load_user(user_id):
    print("HELLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOO", user_id)
    user = db_get_user(user_id)
    print(user)
    return user


@app.route("/")
def home():
    return render_template("home.html")


# @app.route('/blogs/<id>')
# def blog(id):
#   return f"This is blog {id}"


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    if form.is_submitted():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password1.data)
        for i in range(10):
            print(user)
        db_add_user(name=user.name, password_hash=user.password_hash, email=user.email)
        return redirect(url_for('login'))
    else:
        return render_template("signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print("this is email", form.email.data)
        print("check", form.email.data == 'ivanmankos@gmail.com')
        try:
            user = db_get_user_by_email(form.email.data)
            if user is not None and user.check_password(form.password.data):
                print("URAAAAAAAAAAAAAA")
                login_user(user)
                next = request.args.get("next")
                print("next", next)

                return redirect(next or url_for('home'))
        except TypeError:
            flash('Invalid email address or Password.')
        except NoSuchEmailError:
            flash('Invalid email address or Password.')


        flash('Invalid email address or Password.')
    return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
