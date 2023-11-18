import requests
from flask import *
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()
cursor1 = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password =request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if not records and username != "" and password != "":
                return render_template('login.html', message="Неверный логин или пароль")
            elif username == '' or password == '':
                return render_template('login.html', message="Какой то элемент не введён")
            elif username == records[0][2] and password == records[0][3]:
                return render_template('account.html', full_name=records[0][1], login=records[0][2],password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':

        name = request.form.get('name')
        login1 = request.form.get('login')
        password = request.form.get('password')

        if login1 != "" and name != "" and password != "":
            cursor.execute("SELECT * FROM service.users WHERE login = %s ",
                           [(str(login1))])
            records = list(cursor.fetchall())
            if records and login1 != "":
                return render_template('registration.html', message='Такой логин занят')
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',
                               (str(name), str(login1), str(password)))
                conn.commit()
                return redirect('/login/')
        elif login1 == "" or password == "" or name == "":
            return render_template('registration.html', message='Надо заполнить все поля перед концом регистрации')
    return render_template('registration.html')