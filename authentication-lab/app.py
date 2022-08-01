from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDAXCjn6ykUh8yCJnSIufWWxtrp9mol2zk",
  "authDomain": "cs-group-f-maya.firebaseapp.com",
  "projectId": "cs-group-f-maya",
  "storageBucket": "cs-group-f-maya.appspot.com",
  "messagingSenderId": "530887055942",
  "appId": "1:530887055942:web:e7799007f70e6731764847",
  'measurementId' : "G-1KD78NMD5H" ,
  'databaseURL':'https://cs-group-f-maya-default-rtdb.europe-west1.firebasedatabase.app/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth

@app.route('/', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('signin'))
      except:
        error = "Authentication failed"
  else:
    return render_template('signup.html')



@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = ""
  if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      try:
          login_session['user'] = auth.sigh_in_with_email_and_password(email, password)
          return redirect(url_for('add_tweet'))
      except:
          error = "Authentication failed"
  else:
    return render_template('signin.html')
    



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)