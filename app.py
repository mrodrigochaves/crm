from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password123'
app.config['MYSQL_DATABASE_DB'] = 'fedora_db'
app.config['MYSQL_DATABASE_HOST'] = 'host'
mysql.init_app(app)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/members')
def members():
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM members")
   result = cursor.fetchall()
   return render_template('members.html', members=result)

@app.route('/add_member', methods=['POST'])
def add_member():
   name = request.form['name']
   email = request.form['email']
   phone = request.form['phone']
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
   conn.commit()
   return redirect(url_for('members'))

@app.route('/update_member/<id>', methods=['POST'])
def update_member(id):
   name = request.form['name']
   email = request.form['email']
   phone = request.form['phone']
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("UPDATE members SET name=%s, email=%s, phone=%s WHERE id=%s", (name, email, phone, id))
   conn.commit()
   return redirect(url_for('members'))

@app.route('/delete_member/<id>', methods=['GET'])
def delete_member(id):
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("DELETE FROM members WHERE id=%s", (id,))
   conn.commit()
   return redirect(url_for('members'))

if __name__ == '__main__':
   app.run()

