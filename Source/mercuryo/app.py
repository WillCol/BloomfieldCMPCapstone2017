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
    return redirect(url_for('login'))  # return a string

# LoggedIn page
@app.route('/LoggedIn')
@login_required
def LoggedIn():
	return render_template('index.html')

# inventory page
@app.route('/inventory')
def Inventory():
	dic = {"start": 'beginning'}
	dic.setdefault("def", [])
	dic["def"].append("Device Name")
	dic["def"].append("Description")
	dic["def"].append("Category")
	dic["def"].append("Status")
	dic["def"].append("Location")
	dic["def"].append("Owner")
	dic["def"].append("Date of Deployment")
	dic["def"].append("Go-back Date")
	dic["def"].append("IP Address")
	dic["def"].append("Serial Number")

	db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="Inventory")
	cur = db.cursor()
	cur.execute("Select * from Device")

	rowNum = 0
	for row in cur.fetchall():
		dic.setdefault(rowNum, [])
		dic[rowNum].append(row[0])
		dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
		dic[rowNum].append(row[3])
		dic[rowNum].append(row[4])
		dic[rowNum].append(row[5])
		dic[rowNum].append(row[6])
		dic[rowNum].append(row[7])
		dic[rowNum].append(row[8])
		dic[rowNum].append(row[9])
		rowNum = rowNum + 1	

        return render_template('inventory.html', dic=dic)

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
#		elif request.form['submit'] == 'Search Users':
#			userID = request.form['UserID']
#			cur.execute("SELECT Calendar_TaskID FROM User_has_Calendar WHERE User_UserID=\'"+userID+"\'")
#			for column in cur.fetchall():
#				string = "d" % column[0]
#				result = result+", "+string
#		else:
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
			userName = column[0]
			session['security'] = userType
			session['logged_in'] = True
			session['username'] = userName
			flash('You were just logged in!')
			flash(session['security'])
			return redirect(url_for('LoggedIn'))
			#return render_template('LoggedIn.html', userType=userType)
			#return redirect(url_for('home'))         
	
	error = 'Invalid Credentials. Please, try again.'
    return render_template('login.html', error=error)

# route for handling logout protocol
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	session.pop('security', None)
	flash('You were just logged out!')
	return redirect(url_for('login'))

# generic page for adding tasks
@app.route('/generic', methods=['GET', 'POST'])
@login_required
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
@login_required
def mainTable():
                ## do calcs here, give send dictionary of objects
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("EmployeeID")
                emp["def"].append("EmployeeName")
                emp["def"].append("JobTitle")
                emp["def"].append("EmployeeAddress")
                emp["def"].append("EmployeeDepartment")

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

#user account page
@app.route('/account')
@login_required
def account():
	account = {'uName': 'null',  'fName': 'John', 'lName': 'null', 'role': 'null', 'email': 'null'}
	eID = "null"
	eName = "null"
	userName = session['username']
	cur.execute("Select UserName, EmployeeID from User where UserName = "+userName)
	for column in cur.fetchall():
		account['uName'] = column[0]
		eID = column[1]
	cur.execute("Select EmployeeName, JobTitle, EmployeeEmail from Employee where EmployeeID = "+eID)
	for column in cur.fetchall():
		eName = column[0] 
		account['role'] = column[1]
		account['email'] = column[2]
	eNameS = eName.split(" ")
	fName = eNameS[0]
	lName = eNameS[1]
	account['fName'] = fName
	account['lName'] = lName
	
	return render_template('account.html', account=account)
	  
#new device page
@app.route('/addDevice', methods=['GET', 'POST'])
@login_required
def addDevice():
	dLocation = "Null"
	sNumber = "null"
	deviceName = "null"
	IP = "null"
	owner = "null"
	DoD = "null"
	go_back = "null"
	deviceCategory = "null"
	deviceStatus = "null"
	dStatusInt = 0
	if request.method == 'POST':
		dLocation = request.form("location")
		sNumber = request.form("serialNumber")
		deviceName = request.form("computer")
		IP = request.form("IP")
		IPInt = int(IP)
		owner = request.form("owner")
		DoD = request.form("dateOfDeployment")
		go_back = request.form("go-backDate")
		deviceCategory = request.form("deviceCategory")
		deviceStatus = request.form("deviceStatus")
		if deviceStatus == "On field":
			dStatusInt = 11111
		elif deviceStatus == "Not on field":
			dStatisInt = 22222
		else:
			dStatusInt = 33333
		cur.execute(	"Insert into Device("
					+ " DeviceName"
					+ ",Desc"
					+ ",DeviceCategory"
					+ ",DeviceStatus_StatusID"
					+ ",DeviceLocation"
					+ ",DeviceOwner"
					+ ",DateOfDeployment"
					+ ",Go-Back Date"
					+ ",IPAddress"
					+ ") "  
				+ "VALUES("
				+ deviceName+","
				+ "Serial Number: " + sNumber+","
				+ deviceCategory+","
				+ dStatusInt+","
				+ dLocation+","
				+ owner+","
				+ DoD+","
				+ go_back+","
				+ IPInt
				+ ")")

		return redirect(url_for('mainTable'))
		
	return render_template('account.html')		

#edit account
@app.route('/editAccount', methods=['GET', 'POST'])
@login_required
def editAccount():
        account = {'uName': 'null',  'fName': 'John', 'lName': 'null', 'role': 'null', 'email': 'null'}
        eID = "null"
        eName = "null"
        userName = session['username']
        cur.execute("Select UserName, EmployeeID from User where UserName = "+userName)
        for column in cur.fetchall():
                account['uName'] = column[0]
                eID = column[1]
        cur.execute("Select EmployeeName, JobTitle, EmployeeEmail from Employee where EmployeeID = "+eID)
        for column in cur.fetchall():
                eName = column[0]
                account['role'] = column[1]
                account['email'] = column[2]
        eNameS = eName.split(" ")
        fName = eNameS[0]
        lName = eNameS[1]
        account['fName'] = fName
        account['lName'] = lName
	if request.method == 'POST':
		account['fName'] = request.form("fName")
		account['lName'] = request.form("lname")
		account['role'] = request.form("role")
		account['email'] = request.form("email")
		firstName = account['fName']
		lastName = account['lName']
		fullName = firstName + " " + lastName
		cur.execute("Update Employee "
				+ "set EmployeeName = " + fullName +","
				+ "JobtTitle = " + account['role']+","
				+ "EmployeeEmail + account['email'] where EmployeeID = "+eID)
		return redirect(url_for('account'))
	
	return render_template('editAccount.html', account=account)
 			
#change password
@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
	pWord = "null"
	username = sessions['username']
	if request.method == 'POST':
		pWord = request.form("newPassword")
		cur.execute("Update User set Password = " + pWord + " where UserName = "+username)
		return redirect(url_for('account'))
	
	return render_template('changePassword.html')


	
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
