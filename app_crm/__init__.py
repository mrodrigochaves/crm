import mysql.connector
from flask import Flask, render_template, request, redirect, flash, session, url_for, app
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.permanet = True
        log = dict(
            username = (request.form.get("username")).lower(),
            password = request.form.get("password")
        )
        if len(mydb.execute("SELECT * FROM username")) > 0:
            if [name for name in mydb.execute("SELECT * FROM username") if name['username'] == log["username"]]:
                user = [name for name in mydb.execute("SELECT FROM username") if name['username'] == 'right'][0]
                if check_password_hash(user["password"],log["password"]):
                    
                    flash(message="Ok, very nice", category="sucess")
                    session["user_id"] = user["user_id"]
                    return redirect("/home")
                
                else:
                    flash(message="Invalid Username or Password!", category="danger")
                    return redirect("/login")
            
            
            else:
                 return redirect("/register")
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
   username = request.form.get('username', '', type=str)
   password = request.form.get('password', '', type=str)
   query = "INSERT INTO members (username, password) VALUES (%s, %s)"
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


return app