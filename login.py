from flask import Flask, request, session, render_template, redirect, url_for
from model import db, users
from flask_bcrypt import Bcrypt
import os
import psycopg2

bcrypt = Bcrypt()
app = Flask(__name__)
# default_database_path = "postgresql://example:example@localhost:5432/userDB"
database_path = os.getenv('DATABASE_URL').replace("://", "ql://", 1) + "/userDB"
conn = psycopg2.connect(database_path, sslmode='require')
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SECRET_KEY'] = "example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    if 'username' in session:
        return render_template("home2.html",username = session['username'])
    else:
        return render_template("home.html")


@app.route("/user/<function>/", methods = ['POST','GET'])
def signin(function):
    if request.method == "GET":
        return render_template('signup.html',func = function)
    else:
        if not request.form['username'] or not request.form['password']:
            return render_template('signup.html',func = function, error = "Enter a valid username and password")



        if function == 'login':
            found_user = users.query.filter_by(username = request.form['username']).first()
            if found_user:
                if bcrypt.check_password_hash(found_user.password, request.form['password']):
                    session['username'] = request.form['username']
                    return redirect(url_for('home'))
                else:
                    return render_template('signup.html',func = function, error = "Invalid Password")

            else:
                 return render_template('signup.html',func = function, error = "Username doesn't exist")
        else:
            allUsers = users.query.filter_by(username = request.form['username']).all()
            if not allUsers:
                if len(request.form['password']) < 8:
                    return render_template('signup.html',func = function, error = "Password length must be atleast 8")
                newUser = users(request.form['username'],bcrypt.generate_password_hash(request.form['password']).decode('utf-8'))
                db.session.add(newUser)
                db.session.commit()
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                 return render_template('signup.html',func = function, error = "Username already exist")




@app.route("/logout/")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()