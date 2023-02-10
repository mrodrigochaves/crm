#import mysql.connector
from flask import Flask, render_template, request, redirect, url_for


# mydb = mysql.connector.connect(
#    host = 'localhost',
#    user = 'admin',
#    password = 'Password123!',
#    database = 'fedora_db',

# )

app=Flask(__name__,template_folder='templates')

@app.route("/")
def home(name=None):
    return render_template('./home.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/members')
def members():
   conn = mydb.cursor()
   conn.execute("SELECT * FROM members")
   result = conn.fetchall()
   return render_template('members.html', members=result)

@app.route('/add_member', methods=['POST'])
def add_member():
   name = request.form['name']
   email = request.form['email']
   phone = request.form['phone']
   conn = mysql.connect()
   conn = mydb.cursor()
   conn.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
   conn.commit()
   return redirect(url_for('members'))

@app.route('/update_member/<id>', methods=['POST'])
def update_member(id):
   name = request.form['name']
   email = request.form['email']
   phone = request.form['phone']
   conn = mysql.connect()
   conn = mydb.cursor()
   conn.execute("UPDATE members SET name=%s, email=%s, phone=%s WHERE id=%s", (name, email, phone, id))
   conn.commit()
   return redirect(url_for('members'))

@app.route('/delete_member/<id>', methods=['GET'])
def delete_member(id):
   conn = mysql.connect()
   conn = mydb.cursor()
   conn.execute("DELETE FROM members WHERE id=%s", (id,))
   conn.commit()
   return redirect(url_for('members'))


if __name__ == '__main__':
   app.run(debug=True, port=8051)