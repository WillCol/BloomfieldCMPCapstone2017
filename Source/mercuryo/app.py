# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
import MySQLdb

#import for login required decorator
from functools import wraps

# creating an instance object of our db connection
db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="Inventory")
cur = db.cursor()

# create the application object
app = Flask(__name__)

#Secret key needed for sessions
app.secret_key = "my precious"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

# LoggedIn page
@app.route('/LoggedIn')
@login_required
def LoggedIn():
	return render_template('index.html')

# search page
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	result = ""
	taskID = None
	userID = None
	if request.method == 'POST':
		if request.form['submit'] == 'Search Tasks':
			taskID = request.form['TaskID']
			cur.execute("SELECT User_UserID FROM User_has_Calendar WHERE Calendar_TaskID=\'"+taskID+"\'")
			for column in cur.fetchall():
				#converts values of column[0] to string
				string = "%d" % column[0]
				result = result+", "+string
		elif request.form['submit'] == 'Search Users':
			userID = request.form['UserID']
			cur.execute("SELECT Calendar_TaskID FROM User_has_Calendar WHERE User_UserID=\'"+userID+"\'")
			for column in cur.fetchall():
				string = "d" % column[0]
				result = result+", "+string
		else:
			result = 'Invalid entry.'

	return render_template('search.html', result=result)

@app.route('/welcome')
def welcome():
    return render_template('index.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    sec = 'null'
    error = None
    userType = None
    if request.method == 'POST':
	cur.execute("SELECT UserName, Password, Security FROM User")
	for column in cur.fetchall():
        	if request.form['username'] == column[0] and request.form['password'] == column [1]:
			userType = column[2]
			session['logged_in'] = True
			flash('You were just logged in!')
			return redirect(url_for('LoggedIn'))
			#return render_template('LoggedIn.html', userType=userType)
			#return redirect(url_for('home'))         
	
	error = 'Invalid Credentials. Please, try again.'
    return render_template('login.html', error=error)

# route for handling logout protocol
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('login'))

# generic page
@app.route('/generic', methods=['GET', 'POST'])
def generic():
        #if request.method == 'GET':
        taskID = request.args["id"]
        if request.method == 'POST':
                taskID = request.form["taskID"]
                dateStart = request.form["dateStart"]
                dateComplete = request.form["dateComplete"]
                taskStatus = request.form["taskStatus"]
                taskType = request.form["taskType"]

                return "Request sucessfully submited!!"
        else:

                db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="Inventory")
                cur = db.cursor()
                cur.execute("Select * from Calendar where TaskID = "+taskID)

                task  = {"start" : "beginning"}
                task.setdefault("def", [])
                task["def"].append("Task ID")
                task["def"].append("Date Started")
                task["def"].append("Date Completed")
                task["def"].append("Task Status")
                task["def"].append("Task Type")

                rowNum = 0
                for row in cur.fetchall():
                        task.setdefault(rowNum, [])
                        task[rowNum].append(row[0])
                        task[rowNum].append(row[1])
                        task[rowNum].append(row[2])
                        task[rowNum].append(row[3])
                        task[rowNum].append(row[4])
                        rowNum = rowNum + 1
                return render_template('generic.html', task=task)

# main table
@app.route('/mainTable')
def mainTable():
                ## do calcs here, give send dictionary of objects
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("EmployeeID")
                emp["def"].append("EmployeeName")
                emp["def"].append("JobTitle")
                emp["def"].append("EmployeeAddress")
                emp["def"].append("EmployeeDepartment")

                db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="Inventory")
                cur = db.cursor()
                cur.execute("Select * from Employee")

                rowNum = 0

                for row in cur.fetchall():
                        emp.setdefault(rowNum, [])
                        emp[rowNum].append(row[0])
                        emp[rowNum].append(row[1])
                        emp[rowNum].append(row[2])
                        emp[rowNum].append(row[3])
                        emp[rowNum].append(row[4])
                        rowNum = rowNum + 1
                return render_template('mainTable.html', emp=emp)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
