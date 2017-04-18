# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
import MySQLdb
import sys
#import for login required decorator
from functools import wraps

#dbCon = open("dbconfig.txt","r")
#dbConL = []
#for line in dbCon:
#	dbConL.append(line)
#dbName = dbConL[0]
#dbUser = dbConL[1]
#dbPW = dbConL[2]
#print dbName

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
		sCheck = session['security']
		sSheck = int(sCheck)
		if sCheck > 1: 
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
            deviceID = request.args["id"]
	    dLocation = request.form["DeviceLocation"]
            sNumber = request.form["SerialNumber"]
            deviceName = request.form["DeviceName"]
            IP = request.form["IPAddress"]
            IPInt = int(IP)
            owner = request.form["DeviceOwner"]
  	    desc = request.form["Description"]
            DoD = request.form["DateOfDeployment"]
            go_back = request.form["GoBackDate"]
            deviceCategory = request.form["DeviceCategory"]
            deviceStatus = request.form["deviceStatus"]

	    cur.execute("select StatusID from DeviceStatus where StatusDesc = \'"+deviceStatus+"\'")
            for row in cur.fetchall():
            	deviceStatus = row[0]
            deviceStatus = str(deviceStatus)

	    cur.execute("UPDATE Device SET DeviceName = \'"+deviceName+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET Description = \'"+desc+"\' WHERE DeviceID = "+deviceID)
            cur.execute("UPDATE Device SET DeviceCategory = \'"+deviceCategory+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET DeviceStatus_StatusID = \'"+deviceStatus+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET DeviceLocation = \'"+dLocation+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET DeviceOwner = \'"+owner+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET DateOfDeployment = \'"+DoD+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET GoBackDate = \'"+go_back+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET IPAddress = \'"+IP+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET SerialNumber = \'"+sNumber+"\' WHERE DeviceID = "+deviceID)
		
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
            		dev["data"].append(row[1])
            		dev["data"].append(row[2])
            		dev["data"].append(row[3])
            		dev["data"].append(row[4])
           		dev["data"].append(row[5])
			dev["data"].append(row[6])
			dev["data"].append(row[7])
			dev["data"].append(row[8])
			dev["data"].append(row[9])
			dev["data"].append(row[10])
		
		rowNum = 0
        	dStatusL = {"start": ''}
        	cur.execute("select StatusDesc from DeviceStatus")
        	for row in cur.fetchall():
                	dStatusL.setdefault(rowNum, [])
                	dStatusL[rowNum].append(row[0])
                	rowNum = rowNum + 1		
		
                return render_template('editDevice.html', dev=dev, labels=labels, dStatusL = dStatusL)

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

#user table
@app.route('/userTable')
@login_required
@security_check
def userTable():

        labels = {"start": 'beginning'}
        labels.setdefault("def", [])
        labels["def"].append("UserID")
        labels["def"].append("UserName")
        labels["def"].append("Password")
        labels["def"].append("Employee_Employee")
        labels["def"].append("Security")

        cur.execute("Select * from User")

        dic = {"start": 'beginning'}
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
                dic[rowNum].append(row[2])
                dic[rowNum].append(row[3])
                dic[rowNum].append(row[4])
                rowNum = rowNum + 1

        return render_template('userTable.html', dic=dic, labels=labels)

#employee table
@app.route('/employeeTable')
@login_required
@security_check
def employeeTable():

        labels = {"start": 'beginning'}
        labels.setdefault("def", [])
        labels["def"].append("EmployeeID")
        labels["def"].append("EmployeeName")
        labels["def"].append("JobTitle")
        labels["def"].append("EmployeeAddress")
        labels["def"].append("EmployeeDepartment")
        labels["def"].append("EmployeeEmail")
	labels["def"].append("EmployeePhoneNum")


        cur.execute("Select * from Employee")

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
		pNum = "null"
		empID = str(row[0])
		cur.execute("SELECT PhoneNum FROM Phone WHERE Employee_EmployeeID = "+empID)
		for column in cur.fetchall():
			pNum = column[0]
		dic[rowNum].append(pNum) 
                rowNum = rowNum + 1

        return render_template('employeeTable.html', dic=dic, labels=labels)

#taskType table
@app.route('/taskTypeTable')
@login_required
def taskTypeTable():

        labels = {"start": 'beginning'}
        labels.setdefault("def", [])
        labels["def"].append("TaskType")
        labels["def"].append("TaskDesc")

        cur.execute("Select * from Task")

        dic = {"start": 'beginning'}
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
                rowNum = rowNum + 1

        return render_template('taskTypeTable.html', dic=dic, labels=labels)

#deviceStatus table
@app.route('/deviceStatusTable')
@login_required
def deviceStatusTable():

        labels = {"start": 'beginning'}
        labels.setdefault("def", [])
        labels["def"].append("StatusID")
        labels["def"].append("StatusDesc")

        cur.execute("Select * from DeviceStatus")

        dic = {"start": 'beginning'}
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
                rowNum = rowNum + 1

        return render_template('deviceStatusTable.html', dic=dic, labels=labels)

#admin task table
@app.route('/adminTaskTable')
@login_required
def adminTaskTable():
	labels = {"start": ""}
        labels.setdefault("def", [])
        labels["def"].append("TaskID")
        labels["def"].append("DateStarted")
        labels["def"].append("DateCompleted")
        labels["def"].append("TaskStatus")
        labels["def"].append("TaskType")
        labels["def"].append("ActiveTask")
        labels["def"].append("DateActualCompletion")
        labels["def"].append("DeviceID")
	labels["def"].append("UserID")
    
	dic = {"start": ''}
        rowNum = 0
        cur.execute("SELECT * FROM Calendar")
        for row in cur.fetchall():
        	dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
                dic[rowNum].append(row[2])
                dic[rowNum].append(row[3])
                dic[rowNum].append(row[4])
			
		if row[5] == 1:
                	dic[rowNum].append("yes")
                else:
                        dic[rowNum].append("no")
                dic[rowNum].append(row[6])
		dID = "null"
                cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID = "+str(row[0]))
                for column in cur.fetchall():
                	dID = column[0]
                dic[rowNum].append(column[0])
                rowNum = rowNum + 1
        return render_template('taskTable.html', dic=dic, labels=labels)
		

#dropDownTestPage
@app.route('/dropDownTestPage', methods=["GET", "POST"])
@login_required
def dropDownTestPage():
	if request.method == 'POST':
		taskType = request.form["taskType"]
		return "taskType = "+taskType
	else:
		return render_template('dropDownTestPage.html')



#task table
@app.route('/taskTable')
@login_required
def taskTable():
	uID = session['userID']

        labels = {"start": ""}
        labels.setdefault("def", [])
        labels["def"].append("TaskID")
        labels["def"].append("DateStarted")
        labels["def"].append("DateCompleted")
        labels["def"].append("TaskStatus")
        labels["def"].append("TaskType")
	labels["def"].append("ActiveTask")
	labels["def"].append("DateActualCompletion")
	labels["def"].append("DeviceID")
	labels["def"].append("TaskName")
	labels["def"].append("TaskLocation")	
	taskList = []

        cur.execute("SELECT Calendar_TaskID FROM User_has_Calendar WHERE User_UserID = "+str(uID))
	for row in cur.fetchall():
		taskList.append(row[0])
		
	
        dic = {"start": ''}
        rowNum = 0
        for tasks in taskList:
		taskCheck = rowNum
		cur.execute("SELECT * FROM Calendar where TaskID = "+str(taskList[taskCheck]))
		for row in cur.fetchall():
			dic.setdefault(rowNum, [])
                        dic[rowNum].append(row[0])
                        dic[rowNum].append(row[1])
                        dic[rowNum].append(row[2])
                        dic[rowNum].append(row[3])
                        dic[rowNum].append(row[4])
	
			if row[5] == 1:
                                dic[rowNum].append("yes")
                        else:
                                dic[rowNum].append("no")
                        dic[rowNum].append(row[6])
			dic[rowNum].append(row[7])
			dic[rowNum].append(row[8])
                        dID = "null"
                        cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID = "+str(row[0]))
                        for column in cur.fetchall():
				dID = column[0]
                                dic[rowNum].append(column[0])
			
			
                rowNum = rowNum + 1
	return render_template('taskTable.html', dic=dic, labels=labels)



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
	cur.execute("SELECT UserID, UserName, Password, Security FROM User")
	for column in cur.fetchall():
        	if request.form['username'] == column[1] and request.form['password'] == column [2]:
			userType = column[3]
			print userType
			userName = column[1]
			userID = column[0]
			session['security'] = userType
			session['logged_in'] = True
			session['username'] = userName
			session['userID'] = userID
		#	flash('You were just logged in!')
		#	flash(session[''])
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
	empPhone = "null"
	if request.method == "POST":
		
            	eID = request.args["id"]
                eName = request.form["EmployeeName"]
                jTitle = request.form["JobTitle"]
                eAddress = request.form["EmployeeAddress"]
                ePNumber = request.form["EmployeePhoneNumber"]
                eDepartment = request.form["EmployeeDepartment"]
                email = request.form["EmployeeEmail"]
                
		cur.execute("UPDATE Employee SET EmployeeName = \'"+eName+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET JobTitle = \'"+jTitle+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeAddress = \'"+eAddress+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeDepartment = \'"+eDepartment+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeEmail = \'"+email+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeName = \'"+eName+"\' WHERE EmployeeID = "+eID)

                db.commit()

		cur.execute("UPDATE Phone SET PhoneNum = \'"+ePNumber+"\' WHERE Employee_EmployeeID = "+eID+" AND PhoneNum = "+str(empPhone))
               	
                db.commit()
                return redirect(url_for('employeeTable'))
	else:
		
		eID = request.args["id"]
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
                emp["def"].append("EmployeeID")
                emp["def"].append("EmployeeName")
                emp["def"].append("JobTitle")
                emp["def"].append("EmployeeAddress")
                emp["def"].append("EmployeeDepartment")
		emp["def"].append("EmployeeEmail")
		emp["def"].append("EmployeePhoneNumber")

                cur.execute("SELECT * FROM Employee WHERE EmployeeID = "+eID)

                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
                        emp["data"].append(row[1])
                        emp["data"].append(row[2])
                        emp["data"].append(row[3])
                        emp["data"].append(row[4])
			emp["data"].append(row[5])
		pNumber = {'pNum' : 'null'}
		cur.execute("SELECT PhoneNum from Phone WHERE Employee_EmployeeID = "+eID)
		for column in cur.fetchall():
			emp["data"].append(column[0])
		 	empPhone = column[0]
                return render_template('editEmployee.html', emp=emp)

#edit user
@app.route('/editUser', methods=['GET', 'POST']) 
@login_required
@security_check
def editUser():
        if request.method == "POST":
		uID = request.args["id"]
                uName = request.form["UserName"]
                pWord = request.form["Password"]
                sec = request.form["Security"]
		
        	cur.execute("UPDATE User SET UserName = \'"+uName+"\' WHERE UserID = "+uID)
         	cur.execute("UPDATE User SET Password = \'"+pWord+"\' WHERE UserID = "+uID)
         	cur.execute("UPDATE User SET Security = \'"+sec+"\' WHERE UserID = "+uID)
         

                db.commit()
                return redirect(url_for('userTable'))
	else:
		uID = request.args['id']
                emp = {"start" : "beginning"}
                emp.setdefault("def", [])
		emp["def"].append("User ID")
                emp["def"].append("Username")
                emp["def"].append("Password")
                emp["def"].append("Employee ID")
                emp["def"].append("Security")

		cur.execute("SELECT * FROM User WHERE UserID = "+uID)

       

                for row in cur.fetchall():
			emp.setdefault("data", [])
                        emp["data"].append(row[0])
                        emp["data"].append(row[1])
                        emp["data"].append(row[2])
                        emp["data"].append(row[3])
			emp["data"].append(row[4])
          
                return render_template('editUser.html', emp=emp)

#edit task
@app.route('/edittask', methods=['GET', 'POST'])
@login_required
@security_check
def edittask():
	
	tID = request.args["id"]
	devID = 0
        if request.method == "POST":
             
		cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID ="+tID)

                for row in cur.fetchall():
                	devID = row[0]

		nTask = request.form["TaskName"]
		lTask = request.form["TaskLocation"]               
                dStart = request.form["DateStarted"]
                dComp = request.form["DateCompleted"]
                tStatus = request.form["TaskStatus"]
                tType = request.form["TaskType"]
		aTask = request.form["ActiveTask"]
		acDate = request.form["ActualCompletionDate"]
                device = request.form["DeviceID"]
		
		cur.execute("select TaskType from Task where TaskDesc = \'"+tType+"\'")
                for row in cur.fetchall():
                        tType  = row[0]
                tType = str(tType)

				
		                
		cur.execute("UPDATE Calendar SET DateStart = \'"+dStart+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET DateComplete = \'"+dComp+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET TaskStatus = \'"+tStatus+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET Task_TaskType = \'"+tType+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET ActiveTask = \'"+aTask+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET DateActualCompletion = \'"+acDate+"\' WHERE TaskID = "+tID)		
		cur.execute("UPDATE Calendar SET TaskName = \'"+nTask+"\' WHERE TaskID = "+tID)
		cur.execute("UPDATE Calendar SET TaskLocation = \'"+lTask+"\' WHERE TaskID = "+tID)
                db.commit()
		
		cur.execute("UPDATE Device_has_Calendar SET Device_DeviceID = \'"+device+"\' WHERE Calendar_TaskID = "+str(tID)+" AND Device_DeviceID = "+str(devID))

                db.commit()

                return redirect(url_for('taskTable'))
        else:
                tID = request.args['id']
               	emp = {"start": "beginning"}
                cur.execute("SELECT DateStart, DateComplete, TaskStatus, Task_TaskType, ActiveTask, DateActualCompletion, TaskName, TaskLocation"
				+" FROM Calendar WHERE TaskID = "+tID)
		
                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
                        emp["data"].append(row[1])
                        emp["data"].append(row[2])
                        emp["data"].append(row[3])
			emp["data"].append(row[4])
			emp["data"].append(row[5])
			emp["data"].append(row[6])
			emp["data"].append(row[7])

                cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID ="+tID)

		for row in cur.fetchall():
			emp["data"].append(row[0])
			devID = row[0] 
                
		rowNum = 0
	        device = {"start": ''}
        	cur.execute("select DeviceID from Device")
        	for row in cur.fetchall():
                	device.setdefault(rowNum, [])
                	device[rowNum].append(row[0])
                	rowNum = rowNum + 1

        	rowNum = 0
        	task = {"start": ''}
        	cur.execute("select TaskDesc from Task")
        	for row in cur.fetchall():
                	task.setdefault(rowNum, [])
                	task[rowNum].append(row[0])
                	rowNum = rowNum + 1

		
		return render_template('edittask.html', emp=emp, task = task, device = device)

#edit tasktype
@app.route('/edittasktype', methods=['GET', 'POST'])
@login_required
@security_check
def edittasktype():
	
        if request.method == "POST":
		ttID = request.args['id']
                tDesc = request.form["TaskDesc"]
                cur.execute("UPDATE Task SET TaskDesc = \'"+tDesc+"\' WHERE TaskType = "+ttID)
                db.commit()
                return redirect(url_for('taskTypeTable'))
	else:
                ttID = request.args['id']
                emp = {"start" : "beginning"}
             
                cur.execute("SELECT TaskDesc FROM Task WHERE TaskType = "+ttID)
           
                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
                       
                return render_template('edittasktype.html', emp=emp)

#edit device status
@app.route('/editdevicestatus', methods=['GET', 'POST'])
@login_required	
@security_check
def editdevicestatus():
        if request.method == "POST":
		dID = request.args['id']
                sDesc = request.form["StatusDesc"]

		cur.execute("UPDATE DeviceStatus SET StatusDesc = \'"+sDesc+"\' WHERE StatusID = "+dID)
                
                db.commit()
                return redirect(url_for('deviceStatusTable'))
	else:
		dID = request.args['id']
		emp = {"start" : "beginning"}
		emp.setdefault("def", [])
                emp["def"].append("Status Description")

                cur.execute("SELECT StatusDesc FROM DeviceStatus WHERE StatusID = "+dID)

                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
            
                return render_template('editdevicestatus.html', emp=emp)


#user account page
@app.route('/myAccountPage')
@login_required
def account():
	# account dictionary for employee info
	account = {'uName': 'null', 'eName': 'null', 'role': 'null', 'email': 'null', 'address' : 'null', 'phone' : 'null'}
	eID = "null"
	eName = "null"
	userName = session['username']
	account['uName'] = userName
	cur.execute("select Employee_EmployeeID from User where UserName = \'"+userName+"\'")
	for column in cur.fetchall():
		eID = column[0]
	
	cur.execute("Select EmployeeName, JobTitle, EmployeeEmail, EmployeeAddress from Employee where EmployeeID = "+str(eID))
	for column in cur.fetchall():
		account['eName'] = column[0] 
		account['role'] = column[1]
		account['email'] = column[2]
		account['address'] = column[3]
	
	cur.execute("Select PhoneNum from Phone WHERE Employee_EmployeeID = "+str(eID))
	for column in cur.fetchall():
		account['phone'] = column[0]
	
	#active dictionary for user tasks
	active = {'start' : ""}
	cur.execute("select distinct Calendar_TaskID, TaskDesc, DateComplete from User_has_Calendar, User, Task, Calendar" 
			+" where User_UserID = UserID and Calendar_TaskID = TaskID and Task_TaskType = TaskType and UserName = \'"+userName+"\'"
			+" and ActiveTask = 1")
	rowNum = 0
	for column in cur.fetchall():
		active.setdefault(rowNum, [])
		active[rowNum].append(column[0])
		active[rowNum].append(column[1])
		active[rowNum].append(column[2])
		rowNum = rowNum + 1

	#deactive dictionary for user tasks
	deactive = {'start' : ""}
        cur.execute("select distinct Calendar_TaskID, TaskDesc, DateComplete from User_has_Calendar, User, Task, Calendar"
                        +" where User_UserID = UserID and Calendar_TaskID = TaskID and Task_TaskType = TaskType and UserName = \'"+userName+"\'"
                        +" and ActiveTask = 0")
        row = 0
        for column in cur.fetchall():
                deactive.setdefault(row, [])
                deactive[row].append(column[0])
                deactive[row].append(column[1])
                deactive[row].append(column[2])
                row = row + 1
	
	

	return render_template('myAccountPage.html', account=account, active=active, deactive=deactive)
	  
#add employee
@app.route('/addemployee', methods=['GET', 'POST'])
@login_required
@security_check
def addemployee():
	if request.method == "POST":
		
		eName = request.form["EmployeeName"]
		jTitle = request.form["JobTitle"]
		eAddress = request.form["EmployeeAddress"]
		ePNumber = request.form["EmployeePhoneNumber"]
		eDepartment = request.form["EmployeeDepartment"]
		email = request.form["EmployeeEmail"]
	    	
		cur.execute("INSERT INTO Employee (EmployeeName, JobTitle, EmployeeAddress, EmployeeDepartment, EmployeeEmail)"
				+" VALUES (\'"+eName+"\',\'"+jTitle+"\',\'"+eAddress+"\',\'"+eDepartment+"\',\'"+email+"\'"+")")
		db.commit()
		
		cur.execute("select EmployeeID from Employee where EmployeeEmail = \'"+email+"\'")
		eID = "null"	
		for row in cur.fetchall():
			eID = row[0]
		cur.execute("INSERT INTO Phone (PhoneNum, Employee_EmployeeID)"
				+" VALUES (\'"+ePNumber+"\',"+"\'"+str(eID)+"\')")
		db.commit()
		return redirect(url_for('employeeTable'))
		
	return render_template('addemployee.html')

#add user
@app.route('/adduser', methods=['GET', 'POST'])
@login_required
@security_check
def adduser():
	if request.method == "POST":
		uName = request.form["UserName"]
		pWord = request.form["Password"]
		sec = request.form["Security"]
		eID = request.form["EmployeeID"]
		
		cur.execute("select EmployeeID from Employee where EmployeeName = \'"+eID+"\'")
         	for row in cur.fetchall():
        	       	eID = row[0]
            	eID = str(eID)
		
		cur.execute("INSERT INTO User (UserName, Password, Employee_EmployeeID, Security)"
				+" VALUES("
				+"\'"+uName+"\',"
				+"\'"+pWord+"\',"
				+"\'"+eID+"\',"
				+"\'"+sec+"\'"
				+")")
		db.commit()
		return redirect(url_for('userTable'))
	
	rowNum = 0
        name = {"start": ''}
        cur.execute("select EmployeeName from Employee")
        for row in cur.fetchall():
        	name.setdefault(rowNum, [])
        	name[rowNum].append(row[0])
        	rowNum = rowNum + 1
	
	return render_template('adduser.html', name = name)

#add task
@app.route('/addtask', methods=['GET', 'POST'])
@login_required
@security_check
def addtask():
	uID = session["userID"]
        if request.method == "POST":
                #taskID = request.form["TaskID"]
		taskID = 0
                dStart = request.form["DateStarted"]
                dComp = request.form["DateCompleted"]
                tStatus = request.form["TaskStatus"]
		tType = request.form["TaskType"]
		acDate = "0000-00-00"
		device = request.form["DeviceID"]
		aTask = request.form["activeTask"]
		nTask = request.form["TaskName"]
		lTask = request.form["TaskLocation"]		

		cur.execute("select TaskType from Task where TaskDesc = \'"+tType+"\'")
		for row in cur.fetchall():
			tType = row[0]
		tType = str(tType)
	
		cur.execute("INSERT INTO Calendar (DateStart, DateComplete, TaskStatus, Task_TaskType, ActiveTask, DateActualCompletion, TaskName, TaskLocation)"
                                +" VALUES(\'"+dStart+"\',"+"\'"+dComp+"\',"+"\'"+tStatus+"\',"+"\'"+tType+"\',"+"\'"+aTask+"\',"+"\'"+acDate+"\',"+
				"\'"+nTask+"\',"+"\'"+lTask+"\')")
		db.commit()
		
		cur.execute("select TaskID from Calendar order by TaskID DESC limit 1")
		for row in cur.fetchall():
			taskID = row[0]
		taskID = str(taskID)	
		cur.execute("INSERT INTO User_has_Calendar (User_UserID, Calendar_TaskID)"
				+" VALUES("
                                +"\'"+str(uID)+"\',"
                                +"\'"+taskID+"\'"
				+")")
                db.commit()
		
		cur.execute("INSERT INTO Device_has_Calendar (Device_DeviceID, Calendar_TaskID)"
				+" VALUES("
                                +"\'"+device+"\',"
                                +"\'"+taskID+"\'"
                                +")")
		db.commit()

		return redirect(url_for('taskTable'))
	rowNum = 0
        device = {"start": ''}
        cur.execute("select DeviceID from Device")
        for row in cur.fetchall():
                device.setdefault(rowNum, [])
                device[rowNum].append(row[0])
                rowNum = rowNum + 1

	rowNum = 0
        task = {"start": ''}
        cur.execute("select TaskDesc from Task")
        for row in cur.fetchall():
                task.setdefault(rowNum, [])
                task[rowNum].append(row[0])
                rowNum = rowNum + 1

	return render_template('addtask.html', task = task, device = device)


#add taskType
@app.route('/addtasktype', methods=['GET', 'POST'])
@login_required
@security_check
def addtasktype():
	if request.method == "POST":
		#ttID = request.form["TaskTypeID"]
		tDesc = request.form["TaskDesc"]
		cur.execute("INSERT INTO Task (TaskDesc)"
				+" VALUES("
				#+"\'"+ttID+"\',"
				+"\'"+tDesc+"\'"
				+")")
		db.commit()
		return redirect(url_for('taskTypeTable'))
	
	return render_template('addtasktype.html')

#add deviceStatus
@app.route('/adddevicestatus', methods=['GET', 'POST'])
@login_required
@security_check
def adddevicestatus():
	if request.method == "POST":
                sDesc = request.form["StatusDesc"]
                cur.execute("INSERT INTO DeviceStatus (StatusDesc)"
                                +" VALUES("
                                +"\'"+sDesc+"\'"
                                +")")
                db.commit()
                return redirect(url_for('deviceStatusTable'))

        return render_template('adddevicestatus.html')
	
		

#new device page
@app.route('/addDevice', methods=["GET", "POST"])
@login_required
def addDevice():
	if request.method == 'POST':
	
		dLocation = request.form["location"]
        	sNumber = request.form["serialNumber"]
        	deviceName = request.form["computer"]
        	IP = request.form["IP"]
        	owner = request.form["owner"]
		desc = request.form["Desc"]
        	DoD = request.form["dateOfDeployment"]
        	go_back = request.form["backDate"]
        	deviceCategory = request.form["deviceCategory"]
		deviceStatus = request.form["deviceStatus"]
		#deviceID = request.form["deviceID"]

		cur.execute("select StatusID from DeviceStatus where StatusDesc = \'"+deviceStatus+"\'")
		for row in cur.fetchall():
			deviceStatus = row[0]
		deviceStatus = str(deviceStatus)
		cur.execute("INSERT INTO Device (DeviceName, Description, DeviceCategory, DeviceStatus_StatusID, DeviceLocation, DeviceOwner, DateOfDeployment, GoBackDate, IPAddress, SerialNumber)"
					+" VALUES("
					#+"\'"+deviceID+"\',"
					+"\'"+deviceName+"\',"
					+"\'"+desc+"\',"
					+"\'"+deviceCategory+"\',"
					+"\'"+deviceStatus+"\',"
					+"\'"+dLocation+"\',"
					+"\'"+owner+"\',"
					+"\'"+DoD+"\',"
					+"\'"+go_back+"\',"
					+"\'"+IP+"\',"
					+"\'"+sNumber+"\'"
					+")")		
		db.commit()
		
        	return redirect(url_for("Inventory"))
	rowNum = 0
	dStatusL = {"start": ''}
	cur.execute("select StatusDesc from DeviceStatus")
	for row in cur.fetchall():
		dStatusL.setdefault(rowNum, [])
		dStatusL[rowNum].append(row[0])
		rowNum = rowNum + 1
		
	return render_template('addDevice.html', dStatusL = dStatusL)		

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
				+ " EmployeeEmail = \'"+email+"\' where EmployeeID = \'"+eID+"\'")
		db.commit()
		return redirect(url_for('account'))
	
	return render_template('editAccount.html', account=account)

#delete employee
@app.route('/deleteemployee', methods=['GET', 'POST'])
@login_required
@security_check
def deleteemployee():
	if request.method == 'POST':
		eName = request.form["EmployeeName"]
		cur.execute("Select EmployeeID from Employee WHERE EmployeeName = \'"+eName+"\'")
		for row in cur.fetchall():
			eID = row[0]
		eID = str(eID)

		#eID = request.form["EmployeeID"]
		cur.execute("DELETE FROM User WHERE Employee_EmployeeID = "+eID)
		cur.execute("DELETE FROM Employee where EmployeeID = "+eID)
		db.commit()
		cur.execute("DELETE FROM Phone WHERE Employee_EmployeeID = "+eID)
		db.commit() 
		return redirect(url_for('employeeTable'))
	cur.execute("SELECT EmployeeName from Employee")
	emp = {}
	for row in cur.fetchall():
		emp.setdefault(row, "")
		emp[row] = row[0]	
	return render_template('deleteemployee.html', emp = emp)

#delete user
@app.route('/deleteuser', methods=['GET', 'POST'])
@login_required
@security_check
def deleteuser():
        if request.method == 'POST':
		username = request.form["username"]
		cur.execute("select UserID from User where UserName = \'"+username+"\'")
		for row in cur.fetchall():
			uID = row[0]
		uID = str(uID)
                #uID = request.form["UserID"]
		cur.execute("DELETE FROM User_has_Calendar WHERE User_UserID = "+uID)
                cur.execute("DELETE FROM User WHERE UserID = "+uID)
                db.commit()
                return redirect(url_for('userTable'))
	cur.execute("select UserName from User")
	user = {}
	for row in cur.fetchall():
		user.setdefault(row, "")
		user[row] = row[0]
        return render_template('deleteuser.html', user = user)

#delete Calendar Task
@app.route('/deleteCalendarTask', methods=['GET', 'POST'])
@login_required
@security_check
def deleteCalendarTask():
        if request.method == 'POST':
		tName = request.form["TaskName"]
		cur.execute("SELECT TaskID from Calendar WHERE TaskName = \'"+tName+"\'")
		#tID = request.form["taskID"]
		for row in cur.fetchall():
			tID = row[0]
		tID = str(tID)
                cur.execute("DELETE FROM User_has_Calendar WHERE Calendar_TaskID = "+tID)
                db.commit()
                cur.execute("DELETE FROM Device_has_Calendar WHERE Calendar_TaskID ="+tID)
                db.commit()
                cur.execute("DELETE FROM Calendar WHERE TaskID = "+tID)
                db.commit()
                return redirect(url_for('taskTable'))
	
	username = session['username']
	
	cur.execute("select TaskName from Calendar, User_has_Calendar, User where User_UserID = UserID and TaskID = Calendar_TaskID and UserName = \'"+username+"\'") 	
	taskList = {"start" : ""}
	for row in cur.fetchall():
		taskList.setdefault(row, [])
		taskList[row].append(row[0])
	
        return render_template('deleteCalendarTask.html', taskList = taskList)

#delete device
@app.route('/deleteDevice', methods=['GET', 'POST'])
@login_required
@security_check
def deleteDevice():
        if request.method == 'POST':
		sNumber = request.form["SerialNumber"]
		cur.execute("SELECT DeviceID from Device WHERE SerialNumber = "+str(sNumber))
		for row in cur.fetchall():
			dID = row[0]

		#dID = request.form["deviceID"]
		dID = str(dID)
		cur.execute("DELETE FROM Device_has_Calendar WHERE Device_deviceID = "+dID)
                cur.execute("DELETE FROM Device WHERE deviceID = "+dID)
                db.commit()
		return redirect(url_for('Inventory'))

	device = {}
	cur.execute("SELECT SerialNumber from Device")
	for row in cur.fetchall():
		device.setdefault(row, "")
		device[row] = row[0]

        return render_template('deleteDevice.html', device = device)


#delete deviceStatus
@app.route('/deleteDeviceStatus', methods=['GET', 'POST'])
@login_required
@security_check
def deleteDeviceStatus():
        if request.method == 'POST':
		status = request.form["DeviceStatus"]
		cur.execute("SELECT StatusID from DeviceStatus WHERE StatusDesc = \'"+status+"\'")
		sID = 0
		for row in cur.fetchall():
			sID = row[0]
                cur.execute("DELETE FROM DeviceStatus WHERE StatusID = "+str(sID))
                db.commit()
                return redirect(url_for('deviceStatusTable'))
	
	cur.execute("SELECT StatusDesc from DeviceStatus")
	dStatus = {}
	for row in cur.fetchall():
		dStatus.setdefault(row, "")
		dStatus[row] = row[0]

        return render_template('deleteDeviceStatus.html', dStatus = dStatus)

#delete TaskType
@app.route('/deleteTaskType', methods=['GET', 'POST'])
@login_required
@security_check
def deleteTaskType():
        if request.method == 'POST':
		tDesc = request.form["TaskDesc"]
		
                #tID = request.form["taskType"]
                cur.execute("DELETE FROM Task WHERE TaskDesc = \'"+tDesc+"\'")
                db.commit()
                return redirect(url_for('taskTypeTable'))
	cur.execute("SELECT TaskDesc from Task")
	task = {}
	for row in cur.fetchall():
		task.setdefault(row, "")
		task[row] = row[0]
        return render_template('deleteTaskType.html', task = task)
 			
#change password
@app.route('/editPassword', methods=['GET', 'POST'])
@login_required
def editPassword():
	pWord = "null"
	username = session['username']
	if request.method == 'POST':
		opWord = request.form["OldPassword"]
		pWord = request.form["NewPassword"]
		rpWord = request.form["RetypePassword"]

		if(pWord == rpWord):
			cur.execute("Update User set Password = \'" + pWord + "\' where UserName = \'"+username +"\' and Password = \'"+pWord+"\'")
			db.commit()
		return redirect(url_for('account'))
	
	return render_template('editPassword.html')

#userPage
@app.route('/userPage', methods=['GET', 'POST'])
@login_required
@security_check
def userPage():
	return render_template('userPage.html')




#Calendar
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
	
	cur.execute("select TaskID, DateStart, TaskDesc, TaskStatus, TaskName, TaskLocation from Calendar, Task "
			+"where Calendar.Task_TaskType = Task.TaskType and DateStart != '0000-00-00'")
        dic = {"start": "beginning"}
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
		dic[rowNum].append(row[3])
		dic[rowNum].append(row[4])
		dic[rowNum].append(row[5])
                rowNum = rowNum + 1
	
	cur.execute("select TaskID, DateComplete, TaskDesc, TaskStatus, TaskName, TaskLocation from Calendar, Task "
                        +"where Calendar.Task_TaskType = Task.TaskType and DateComplete != '0000-00-00'")
        dic2 = {"start": "beginning"}
        num = 0
        for column in cur.fetchall():
                dic2.setdefault(num, [])
                dic2[num].append(column[0])
                dic2[num].append(column[1])
                dic2[num].append(column[2])
                dic2[num].append(column[3])
		dic2[num].append(column[4])
                dic2[num].append(column[5])
		num = num + 1
	

        return render_template('calendar.html', dic=dic, dic2=dic2)
	
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded = True, debug = False)
