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
auth = firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
      name = request.form['name']
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      bio = request.form['bio']

      try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)

        user= {'name':name,'username':username,'email':email,'password':password,'bio':bio}
        db.child('Users').child(login_session['user']['localId']).set(user)
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
          login_session['user'] = auth.sign_in_with_email_and_password(email, password)
          return redirect(url_for('add_tweet'))
      except:
          error = "Authentication failed"
  else:
    return render_template('signin.html')
    



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
  #name = login_session['name']
  if request.method=='POST':
    try:
      title = request.form['title']
      tweet = request.form['tweet']
      uid = login_session['user']['localId']
      tweets = {"title":title,"tweet":tweet,"uid":uid}
      db.child('tweets').push(tweets)
      return redirect(url_for('all_tweets'))

    except:
      raise
      error = "couldn't post tweet"

  else:
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET','POST'])
def all_tweets():
  if request.method=='POST':
    try:
      redirect(url_for('add_tweet'))

    except:
      error = "coldn't open tweets"

  else:
    tweets=db.child('tweets').get().val()
    return render_template('tweets.html',tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)