from flask import Flask, render_template, flash, request, session, redirect, url_for
import random, string
import db
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db_file = 'users.db'
db = db.database(db_file)

def randomstr(length):
   letters = string.ascii_letters + string.digits
   return ''.join(random.choice(letters) for i in range(length))

@app.route('/')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET'])
def login():
    print(request.form.get('login_failed'))
    if request.args.get('login_failed'):
        return render_template('login.html', error='error')
    elif request.args.get('verify_failed'):
        return render_template('login.html', verifyfailed='verifyfailed')
    else:
        return render_template('login.html')

@app.route('/loginattempt', methods=['GET', 'POST'])
def loginattempt():
    verify_pass = db.verify_password(request.form['username'], request.form['password'])
    if verify_pass:
        session['password_ok'] = True
        session['username'] = request.form['username']
        return redirect(url_for('verify'))
    else:
        return redirect(url_for('login') + '?login_failed=true')

@app.route('/verify')
def verify():
    if not session.get('password_ok'):
        return redirect(url_for('login'))
    message = randomstr(20)
    session['message'] = message
    return render_template('verify.html', message=message)

@app.route('/verifyattempt', methods=['POST'])
def verifyattempt():
    if db.verify_signature(session['username'], session['message'], request.form['signature']):
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        session.clear()
        return redirect(url_for('login') + '?verify_failed=true')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    if not db.isadmin(session['username']):
        return redirect(url_for('/'))

    