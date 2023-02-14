import mysql.connector
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, template_folder='templates')
config = {
    'user': 'admin',
    'password': 'Password123!',
    'host': '127.0.0.1',
    'database': 'fedora_db'
}
mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
   username = request.form.get('username', '', type=str)
   password = request.form.get('secret', '', type=str)
   query = "INSERT INTO members (username, secret) VALUES (%s, %s)"
   values = (username,password)
   cursor.execute(query, values)
   mydb.commit()
   return render_template('register.html')

@app.route('/members')
def members():
    query = "SELECT * FROM members"
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('members.html', members=result)

@app.route('/add_member', methods=['POST'])
def add_member():
    username = request.form.username.data['username']
    email = request.form.email.data['email']
    phone = request.form.phone.data['phone']
    query = "INSERT INTO members (username, email, phone) VALUES (%s, %s, %s)"
    values = (username, email, phone)
    cursor.execute(query, values)
    mydb.commit()
    return redirect(url_for('members'))

@app.route('/update_member/<id>', methods=['POST'])
def update_member(id):
    username = request.form.username.data['username']
    email = request.form.email.data['email']
    phone = request.form.phone.data['phone']
    query = "UPDATE members SET username=%s, email=%s, phone=%s WHERE id=%s"
    values = (username, email, phone, id)
    cursor.execute(query, values)
    mydb.commit()
    return redirect(url_for('members'))

@app.route('/delete_member/<id>', methods=['GET'])
def delete_member(id):
    query = "DELETE FROM members WHERE id=%s"
    values = (id,)
    cursor.execute(query, values)
    mydb.commit()
    return redirect(url_for('members'))


if __name__ == '__main__':
   app.run(debug=True, port=8051)