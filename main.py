from flask import Flask, render_template, redirect, request, session
import mysql.connector
import json

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
        cursor.execute("SELECT * FROM userdetail WHERE email ='" +
                       username + "' and  password = '" + password + "'")
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
    cursor.execute("SELECT club_name from eventsdetails")
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
            cursor.execute('INSERT INTO eventsdetails(club_name, email, phone, service, event_name, details) values(%s, %s, %s, %s, %s, %s)',
                           (club, email, phone, service, name, details))
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


@app.route('/register')
def register():
    cursor.execute("SELECT event_name, status from eventsdetails")
    data = cursor.fetchall()
    print(data)
    return render_template('register.html', posts=data)


@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/singleblog/<event>')
def singleblog(event):
    print(event)
    cursor.execute(
        "SELECT event_name, club_name, service, email, phone, details from eventsdetails WHERE event_name='"+event+"';")
    data = cursor.fetchone()
    print(data)
    return render_template('singleblog.html', posts=data)


# ==== api ====
@app.route('/mlogin', methods=['GET', 'POST'])
def mlogin():
    if request.method == 'POST':
        content = request.data
        print(type(content))
        print(content)
        my_json = content.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        print(data)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        print(type(data))
        print(data["email"])

        email = data['email']
        password = data['password']
        # flag = content['flag']
        # fcm_token = content['fcm_token']
        # cursor.execute("SELECT * FROM userdetail WHERE email ='" +
        #                email + "' and  password = '" + password + "'")
        # re = cursor.fetchone()

        re = None
        print(re)
        if re is None:
            data = {
                "value": 0,
                "message": "not ok",
                "clubs": "",
                "details": "",
                "id": ""
            }
            y = json.dumps(data)
            return y
        else:
            cursor.execute("SELECT event_name from eventsdetails")
            data = cursor.fetchall()
            cursor.execute("SELECT details from eventsdetails")
            data2 = cursor.fetchall()
            cursor.execute("SELECT status from eventsdetails")
            data3 = cursor.fetchall()
            cursor.execute("SELECT club_id from eventsdetail")
            data4 = cursor.fetchall()
            # session['user'] = username
            data = {
                "value": 1,
                "message": "ok",
                "events": data,
                "event_details": data2,
                "event_statuses": data3,
                "id": data4
            }
            y = json.dumps(data)
            return y
    return "wrong method"


@app.route('/mevents', methods=['GET', 'POST'])
def mevents():
    cursor.execute(
        "SELECT event_name, club_name, service, email, phone, details from eventsdetails")
    data = cursor.fetchall()
    print(data)
    y = json.dumps(data)
    return y


# ====     ====


if __name__ == '__main__':
    app.run(debug=True)
