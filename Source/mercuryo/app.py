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

#security decorator
def security_check(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['security'] > 1:
		return f(*args, **kwargs)
	else:
	return redirect(url_for('Inventory'))
	return wrap

# use decorators to link the function to a url
@app.route('/')
def home():
    return redirect(url_for('login'))  # return a string

# edit Device page
@app.route('/editDevice', methods=["GET", "POST"])
@login_required
def editDevice():
        if request.method == 'POST':
         
	    dLocation = request.form["location"]
            sNumber = request.form["serialNumber"]
            deviceName = request.form["computer"]
            IP = request.form["IP"]
            IPInt = int(IP)
            owner = request.form["owner"]
  	    desc = request.form["Desc"]
            DoD = request.form["dateOfDeployment"]
            go_back = request.form["go-backDate"]
            deviceCategory = request.form["deviceCategory"]
            deviceStatus = request.form["deviceStatus"]
	    deviceID = request.form["deviceID"]
	    cur.execute("UPDATE Device SET DeviceName = \'"+deviceName+"\' WHERE DeviceID =\'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET Description = \'"+desc+"\' WHERE DeviceID = \'"+deviceID+"\'")
            cur.execute("UPDATE Device SET DeviceCategory = \'"+deviceCategory+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET DeviceStatus_StatusID = \'"+deviceStatus+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET DeviceLocation = \'"+dLocation+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET DeviceOwner = \'"+owner+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET DateOfDeployment = \'"+DoD+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET GoBackDate = \'"+go_back+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET IPAddress = \'"+IP+"\' WHERE DeviceID = \'"+deviceID+"\'")
	    cur.execute("UPDATE Device SET SerialNumber = \'"+sNumber+"\' WHERE DeviceID = \'"+deviceID+"\'")
		
	    db.commit()
		
            return redirect(url_for("Inventory"))
        
	else:
		devID = request.args["id"]
                cur.execute("Select * from Device where DeviceID = "+devID)

		labels = {"start": 'beginning'}
        	labels.setdefault("def", [])
        	labels["def"].append("Device Name")
        	labels["def"].append("Description")
        	labels["def"].append("Category")
        	labels["def"].append("Status")
        	labels["def"].append("Location")
        	labels["def"].append("Owner")
        	labels["def"].append("Date of Deployment")
        	labels["def"].append("Go-back Date")
        	labels["def"].append("IP Address")
        	labels["def"].append("Serial Number")

		dev = {"start": 'beginning'}

		for row in cur.fetchall():
			dev.setdefault("data", [])
            		dev["data"].append(row[0])
            		dev["data"].append(row[1])
            		dev["data"].append(row[2])
            		dev["data"].append(row[3])
           		dev["data"].append(row[4])
			dev["data"].append(row[5])
			dev["data"].append(row[6])
			dev["data"].append(row[7])
			dev["data"].append(row[8])
			dev["data"].append(row[9])
		
                return render_template('editDevice.html', dev=dev, labels=labels)

# inventory page
@app.route('/inventory')
def Inventory():
		
	labels = {"start": 'beginning'}
	labels.setdefault("def", [])
	labels["def"].append("Device ID")
	labels["def"].append("Device Name")
	labels["def"].append("Description")
	labels["def"].append("Category")
	labels["def"].append("Status")
	labels["def"].append("Location")
	labels["def"].append("Owner")
	labels["def"].append("Date of Deployment")
	labels["def"].append("Go-back Date")
	labels["def"].append("IP Address")
	labels["def"].append("Serial Number")

	cur.execute("Select * from Device")

	dic = {"start": 'beginning'}
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
		dic[rowNum].append(row[10])
		rowNum = rowNum + 1	

        return render_template('inventory.html', dic=dic, labels=labels)

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
			return redirect(url_for('Inventory'))
	
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

#edit employee
@app.route('/editEmployee', methods=['GET', 'POST'])
@login_required
@security_check
def editEmployee():
	if request.method == "POST":
                cur.execute("SELECT EmployeeID WHERE EmployeeEmail = "+email)
                for column in cur.fetchall():
                        eID = column[0]
                eName = request.form["EmployeeName"]
                jTitle = request.form["JobTitle"]
                eAddress = request.form["EmployeeAddress"]
                ePNumber = request.form["EmployeePhoneNumber"]
                eDepartment = request.form["EmployeeDepartment"]
                email = request.form["Email"]
                cur.execute("UPDATE Phone SET (EmployeeName, JobTitle, EmployeeAddress,"
                                +" EmployeeDepartment, EmployeeEmail)"
                                +" VALUES("
                                +"\'"+eName+"\',"
                                +"\'"+jTitle+"\',"
                                +"\'"+eAddress+"\',"
                                +"\'"+email+"\'"
                                +") WHERE EmployeeID = \'"+eID+"\'")
                db.commit()
                cur.execute("UPDATE Phone SET (PhoneNum, Employee_EmployeeID)"
                                +" VALUES("
                                +"\'"+ePNumber+"\',"
                                +"\'"+eID+"\'"
                                +") WHERE Employee_EmployeeID = \'"+eID+"\'")
                db.commit()
                return redirect(url_for('employeeTable'))
	else:
		eID = request.args["'id"
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("EmployeeID")
                emp["def"].append("EmployeeName")
                emp["def"].append("JobTitle")
                emp["def"].append("EmployeeAddress")
                emp["def"].append("EmployeeDepartment")
		emp["def"].append("EmployeeEmail")

                cur.execute("SELECT * FROM Employee WHERE EmployeeID = \'"+eID+"\'")

                rowNum = 0

                for row in cur.fetchall():
                        emp.setdefault(rowNum, [])
                        emp[rowNum].append(row[0])
                        emp[rowNum].append(row[1])
                        emp[rowNum].append(row[2])
                        emp[rowNum].append(row[3])
                        emp[rowNum].append(row[4])
			emp[rowNum].append(row[5])
                        rowNum = rowNum + 1
		pNumber = {'pNum' : 'null'}
		cur.execute("SELECT PhoneNum from Phone WHERE Employee_EmployeeID = \'"+eID+"\'")
		for column in cur.fetchall():
			pNumber['pNum'] = column[0]
		 
                return render_template('editEmployee.html', emp=emp, pNumber=pNumber)

#edit user
@app.route('/editUser', methods=['GET', 'POST']) 
@login_required
@security_check
def editUser():
        if request.method == "POST":
		uID = request.args['id']
                uName = request.form["UserName"]
                pWord = request.form["Password"]
                sec = request.form["Security"]
                eID = request.form["EmployeeID"]
                cur.execute("UPDATE User SET(UserName, Password, Employee_EmployeeID, Security)"
                                +" VALUES("
                                +"\'"+uName+"\',"
                                +"\'"+pWord+"\',"
                                +"\'"+eID+"\',"
                                +"\'"+sec+"\'"
                                +") WHERE UserID = \'"+uID+"\'")
                db.commit()
                return redirect(url_for('userTable'))
	else:
		uID = request.args['id']
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("UserName")
                emp["def"].append("Password")
                emp["def"].append("Security")
                emp["def"].append("EmployeeID")

		cur.execute("SELECT UserName, Password, Employee_EmployeeID, Security FROM User WHERE UserID = \'"+uID+"\'")

                rowNum = 0

                for row in cur.fetchall():
                        emp.setdefault(rowNum, [])
                        emp[rowNum].append(row[0])
                        emp[rowNum].append(row[1])
                        emp[rowNum].append(row[2])
                        emp[rowNum].append(row[3])
                        rowNum = rowNum + 1
                return render_template('editUser.html', emp=emp)

#edit tasktype
@app.route('/editTaskType', methods=['GET', 'POST'])
@login_required
@security_check
def editTaskType():
        if request.method == "POST":
		tID = request.args['id']
                tDesc = request.form["TaskDesc"]
                cur.execute("UPDATE Task SET(TaskDesc)"
                                +" VALUES("
                                +"\'"+tDesc+"\'"
                                +") WHERE TaskType = \'"+tID+"\'")
                db.commit()
                return redirect(url_for('taskTable'))
	else:
                tID = request.args['id']
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("TaskDesc")

                cur.execute("SELECT TaskDesc FROM Task WHERE TaskType = \'"+uID+"\'")

                rowNum = 0

                for row in cur.fetchall():
                        emp.setdefault(rowNum, [])
                        emp[rowNum].append(row[0])
                        rowNum = rowNum + 1
                return render_template('editTaskType.html', emp=emp)

#edit device status
@app.route('/editDeviceStatus', methods=['GET', 'POST'])
@login_required	
@security_check
def editDeviceStatus():
        if request.user == "POST":
		dID = request.args['id']
                sDesc = request.form["StatusDesc"]
                cur.execute ("UPDATE DeviceStatus SET (StatusDesc)"
                                +" VALUES("
                                +"\'"+sDesc+"\'"
                                +") WHERE StatusID = \'"+dID+"\'") 
                db.commit()
                return redirect(url_for('statusTable'))
	else:
		dID = request.args['id']
		emp = {"start" : "beginning"}
                emp["def"].append("StatusDesc")

                cur.execute("SELECT StatusDesc FROM DeviceStatus WHERE StatusID = \'"+dID+"\'")

                rowNum = 0

                for row in cur.fetchall():
                        emp.setdefault(rowNum, [])
                        emp[rowNum].append(row[0])
                        rowNum = rowNum + 1
                return render_template('editDeviceStatus.html', emp=emp)


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
	  
#add employee
@app.route('/addemployee', methods=['GET', 'POST'])
@login_required
@security_check
def addemployee():
	if request.method == "POST":
		eID = "null"
		eName = request.form["EmployeeName"]
		jTitle = request.form["JobTitle"]
		eAddress = request.form["EmployeeAddress"]
		ePNumber = request.form["EmployeePhoneNumber"]
		eDepartment = request.form["EmployeeDepartment"]
		email = request.form["Email"]
		cur.execute("INSERT INTO Device (EmployeeName, JobTitle, EmployeeAddress,"
				+" EmployeeDepartment, EmployeeEmail)"
				+" VALUES("
				+"\'"+eName+"\',"
				+"\'"+jTitle+"\',"
				+"\'"+eAddress+"\',"
				+"\'"+email+"\'"
				+")")
		db.commit()
		cur.execute("SELECT EmployeeID WHERE EmployeeEmail = "+email)
		for column in cur.fetchall():
			eID = column[0]
		cur.execute("INSERT INTO Phone (PhoneNum, Employee_EmployeeID)"
				+" VALUES("
				+"\'"+ePNumber+"\',"
				+"\'"+eID+"\'"
				+")")
		db.commit()
		return redirect(url_for('employeeTable'))
	
	return render_template('addemployee.html')

#add user
@app.route('/adduser', methods=['GET', 'POST']
@login_required
@security_check
def adduser():
	if request.method == "POST":
		uName = request.form["UserName"]
		pWord = request.form["Password"]
		sec = request.form["Security"]
		eID = request.form["EmployeeID"]
		cur.execute("INSERT INTO User (UserName, Password, Security, Employee_EmployeeID, Security)"
				+" VALUES("
				+"\'"+uName+"\',"
				+"\'"+pWord+"\',"
				+"\'"+eID+"\',"
				+"\'"+sec+"\'"
				+")")
		db.commit()
		return redirect(url_for('userTable'))
	
	return render_template('adduser.html')

#add taskType
@app.route('/addTaskType', methods=['GET', 'POST'])
@login_required
@security_check
def addTaskType():
	if request.method == "POST":
		tDesc = request.form["TaskDesc"]
		cur.execute("INSERT INTO Task (TaskDesc)"
				+" VALUES("
				+"\'"+tDesc+"\'"
				+")")
		db.commit()
		return redirect(url_for('taskTable'))
	
	return render_template('addTaskType.html')

#add deviceStatus
@app.route('/addDeviceStatus', methods=['GET', 'POST')
@login_required
@security_check
def addDeviceStatus():
	if request.user == "POST":
                sDesc = request.form["StatusDesc"]
                cur.execute("INSERT INTO DeviceStatus (StatusDesc)"
                                +" VALUES("
                                +"\'"+sDesc+"\'"
                                +")")
                db.commit()
                return redirect(url_for('statusTable'))

        return render_template('addDeviceStatis.html')
	
		

#new device page
@app.route('/addDevice', methods=['GET', 'POST'])
@login_required
def addDevice():
	if request.method == "POST":
		dLocation = request.form["location"]
        	sNumber = request.form["serialNumber"]
        	deviceName = request.form["computer"]
        	IP = request.form["IP"]
        	owner = request.form["owner"]
		desc = request.form["Desc"]
        	DoD = request.form["dateOfDeployment"]
        	go_back = request.form["go-backDate"]
        	deviceCategory = request.form["deviceCategory"]
        	deviceStatus = request.form["deviceStatus"]
		deviceID = request.form["deviceID"]
		
		cur.execute("INSERT INTO Device (DeviceName, Description, DeviceCategory," 
					+" DeviceStatus_StatusID, DeviceLocation, DeviceOwner, DateOfDeployment, GoBackDate, IPAddress, SerialNumber)"
					+" VALUES("
					+"\'"+deviceName+"\',"
					+"\'"+desc+"\',"
					+"\'"+deviceCategory+"\',"
					+"\'"+dStatusInt+"\',"
					+"\'"+dLocation+"\',"
					+"\'"+owner+"\',"
					+"\'"+DoD+"\',"
					+"\'"+go_back+"\',"
					+"\'"+IP+"\',"
					+"\'"+sNumber+"\'"
					+")")		
		db.commit()
		
        	return redirect(url_for("Inventory"))
		
	return render_template('addDevice.html')		

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
		role = account['role']
		email = account['email']
		fullName = firstName + " " + lastName
		cur.execute("Update Employee "
				+ "set EmployeeName = \'"+fullName+"\',"
				+ " JobtTitle = \'" +role+"\',"
				+ " EmployeeEmail = \'"+email+"\' where EmployeeID = \'"+eID"\'")
		db.commit()
		return redirect(url_for('account'))
	
	return render_template('editAccount.html', account=account)

#delete employee
@app.route('/deleteEmployee', methods['GET', 'POST'])
@login_required
@security_check
def deleteEmployee():
	if request.method == 'POST':
		eID = request.form["employeeID"]
		cur.execute("DELETE FROM Employee where EmployeeID = \'"+eID+"\'")
		db.commit()
		return redirect(url_for('employeeTable')
	
	return render_template('deleteEmployee.html')

#delete user
@app.route('/deleteUser', methods['GET', 'POST'])
@login_required
@security_check
def deleteUser():
        if request.method == 'POST':
                uID = request.form["userID"]
                cur.execute("DELETE FROM User where UserID = \'"+uID+"\'")
                db.commit()
                return redirect(url_for('userTable')

        return render_template('deleteUser.html')

#delete calendar task

		
 			
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
