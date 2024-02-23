from flask import Flask, render_template, request, redirect, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'your_secret_key'

firebaseConfig = {
  "apiKey": "AIzaSyBarDOGmEnYYitE5a00Lu2YaikXOfDFPzA",
  "authDomain": "sts-3a963.firebaseapp.com",
  "projectId": "sts-3a963",
  "storageBucket": "sts-3a963.appspot.com",
  "messagingSenderId": "292647525098",
  "appId": "1:292647525098:web:bc4cdd77d239581ea31593",
  "measurementId": "G-YX6NN8EVE6",
  "databaseURL": "https://sts-3a963-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public')
def public():
    return render_template('public.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child("users").child(user_id).get().val()
        user_name = user_data['name'] if user_data else 'Unknown'
        return render_template('home.html', user_name=user_name)
    else:
        return redirect('/home')



@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_data = {
            "name": name,
            "email": email
        }
        db.child("users").child(user['localId']).set(user_data)
        return redirect('/public')
    except Exception as e:
        return str(e)

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['user_id'] = user['localId']
        return redirect('/home')
    except Exception as e:
        return str(e)


@app.route('/signout', methods=['POST'])
def signout():
    session.pop('user_id', None)
    return redirect('/public')

if __name__ == '__main__':
    app.run(debug=True)
