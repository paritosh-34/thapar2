from flask import Flask, render_template, redirect, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "super-secret-key"

db = mysql.connector.connect(host='localhost', user='root', database='testing')
cursor = db.cursor()


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        if session['user'] == 'admin':
            return redirect('/event')
        else:
            return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM userdetail WHERE email ='" + username + "' and  password = '" + password + "'")
        data = cursor.fetchone()
        print(data)
        if data is None:
            return render_template('index.html', i='invalid username or password')
        else:
            if data[4] == 'admin':
                session['user'] = 'admin'
                return redirect('/event')
            elif data[4] == 'head':
                session['user'] = 'head'
            else:
                session['user'] = 'student'
            return redirect('/main')
    return render_template('index.html')


@app.route('/main')
def main():
    cursor.execute("SELECT event_name from eventsdetails")
    data = cursor.fetchall()
    cursor.execute("SELECT details from eventsdetails")
    data2 = cursor.fetchall()
    cursor.execute("SELECT status from eventsdetails")
    data3 = cursor.fetchall()
    return render_template('main.html', posts=data, details=data2, l=len(data) - 1, ii=data3)


@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT event_name from eventsdetails")
    data = cursor.fetchall()
    # cursor.close()
    cursor.execute("SELECT club_name from eventsdetails")
    data2 = cursor.fetchall()
    for d in data:
        print(d[0])
        print(type(d))
        # d[0] = d[0].replace("'", "")
        # d[0] = d[0].replace(",", "")
    print(data)
    return render_template('dashboard.html', posts=data, clubs=data2, l=len(data)-1)


@app.route('/category')
def category():
    return render_template('category.html')


@app.route('/event', methods=['GET', 'POST'])
def event():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            service = request.form.get('service')
            club = request.form.get('club')
            details = request.form.get('message')
            cursor.execute('INSERT INTO eventsdetails(club_name, email, phone, service, event_name, details) values(%s, %s, %s, %s, %s, %s)', (club, email, phone, service, name, details))
            db.commit()
        return render_template('event_admin.html')
    return redirect('/login')


@app.route('/events')
def events():
    cursor.execute("SELECT event_name from eventsdetails")
    data = cursor.fetchall()
    print(data)
    return "ok"


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


app.run(host='0.0.0.0', port=4000)
