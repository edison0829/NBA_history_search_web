from firebase import firebase
from flask import Flask
from flask import render_template
from form import FirePut
from flask import request
import flask
import json

app = Flask(__name__, template_folder='page')


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

firebase = firebase.FirebaseApplication('https://sign-up-d8e33.firebaseio.com/', None)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/logInAndSignUp', methods=['GET', 'POST'])
def fireput():
    register_Data = {'Email' : request.form.get('email'),'User name' : request.form.get('username'),'Password' : request.form.get('currentPassword')}
    firebase.post('/',register_Data)
    print request.form
    login_Data = [request.form.get('emailnow'),request.form.get('password')]
    check = firebase.get('/',None)
    keyword=[]
    for key, value in check.iteritems():
        keyword.append([value['Email'],value['Password']])

    if login_Data in keyword:
        return render_template('usersCenter.html')
    else:
        flask.flash('Log-in failed.')
        return render_template('logInAndSignUp.html')

@app.route('/usersCenter')
def center():
    return render_template('usersCenter.html')


if __name__ == '__main__':
    app.run(debug=True)
