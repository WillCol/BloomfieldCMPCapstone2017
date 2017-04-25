# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import MySQLdb
import sys
#import for login required decorator
from functools import wraps

dbCon = open("dbconfig.txt","r")
dbConL = []
for line in dbCon:
	dbConL.append(line)
dbName = dbConL[0]
dbUser = dbConL[1]
dbPW = dbConL[2]
print dbName
print dbPW
print dbUser

# creating an instance object of our db connection
db = MySQLdb.connect(host="localhost",user=dbUser.rstrip(),passwd=dbPW.rstrip(),db=dbName.rstrip())
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

	    cur.execute("select StatusID from DeviceStatus where StatusName = \'"+deviceStatus+"\'")
            for row in cur.fetchall():
            	deviceStatus = row[0]
            deviceStatus = str(deviceStatus)

	    cur.execute("select CategoryID from DeviceCategory where CategoryName = \'"+deviceCategory+"\'")
            for row in cur.fetchall():
                deviceCategory = row[0]
            deviceCategory = str(deviceCategory)

	    cur.execute("UPDATE Device SET DeviceName = \'"+deviceName+"\' WHERE DeviceID = "+deviceID)
	    cur.execute("UPDATE Device SET Description = \'"+desc+"\' WHERE DeviceID = "+deviceID)
            cur.execute("UPDATE Device SET DeviceCategory_CategoryID = \'"+deviceCategory+"\' WHERE DeviceID = "+deviceID)
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
		uName = session['username']
                cur.execute("Select * from Device where DeviceID = "+devID)

		labels = { }
        	labels.setdefault("def", [])
        	labels["def"].append("Device Name")
        	labels["def"].append("Description")
        	labels["def"].append("Category")
        	labels["def"].append("Status")
        	labels["def"].append("Location")
        	labels["def"].append("Owner")
        	labels["def"].append("Date of Deployment (YYYY-MM-DD)")
        	labels["def"].append("Go-back Date(YYYY-MM-DD)")
        	labels["def"].append("IP Address")
        	labels["def"].append("Serial Number")

		dev = { }

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
			dev["data"].append(row[0])	
		rowNum = 0
        	dStatusL = { }
        	cur.execute("select StatusName from DeviceStatus")
        	for row in cur.fetchall():
                	dStatusL.setdefault(rowNum, [])
                	dStatusL[rowNum].append(row[0])
                	rowNum = rowNum + 1		
		
		num = 0
                cat = { }
                cur.execute("select CategoryName from DeviceCategory")
                for row in cur.fetchall():
                        cat.setdefault(num, [])
                        cat[num].append(row[0])
                        num = num + 1

                return render_template('editDevice.html', dev=dev, labels=labels, dStatusL = dStatusL, cat=cat, uName=uName)

# inventory page
@app.route('/inventory')
@login_required
def Inventory():
	uName = session['username']
		
	labels = { }
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

	dic = { }
	rowNum = 0
	for row in cur.fetchall():
		dic.setdefault(rowNum, [])
		dic[rowNum].append(row[0])
		dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
		cur.execute("SELECT CategoryName from DeviceCategory WHERE CategoryID = \'"+str(row[3])+"\'")
		for col in cur.fetchall():
			dic[rowNum].append(col[0])
                cur.execute("SELECT StatusName from DeviceStatus WHERE StatusID = \'"+str(row[4])+"\'")
                for col in cur.fetchall():
                        dic[rowNum].append(col[0])
		dic[rowNum].append(row[5])
		dic[rowNum].append(row[6])
		dic[rowNum].append(row[7])
		dic[rowNum].append(row[8])
		dic[rowNum].append(row[9])
		dic[rowNum].append(row[10])
		rowNum = rowNum + 1	

        return render_template('inventory.html', dic=dic, labels=labels, uName=uName)

#user table
@app.route('/userTable')
@login_required
@security_check
def userTable():
	uName = session['username']
	
        labels = { }
        labels.setdefault("def", [])
        labels["def"].append("UserID")
        labels["def"].append("UserName")
        labels["def"].append("Password")
        labels["def"].append("Employee ID")
        labels["def"].append("Security")

        cur.execute("Select * from User")

        dic = { }
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
                dic[rowNum].append(row[2])
                dic[rowNum].append(row[3])
                dic[rowNum].append(row[4])
                rowNum = rowNum + 1

        return render_template('userTable.html', dic=dic, labels=labels, uName=uName)

#employee table
@app.route('/employeeTable')
@login_required
@security_check
def employeeTable():
	uName = session['username']

        labels = { }
        labels.setdefault("def", [])
        labels["def"].append("Employee ID")
        labels["def"].append("Employee Name")
        labels["def"].append("Job Title")
        labels["def"].append("Employee Address")
        labels["def"].append("Employee Department")
        labels["def"].append("Employee Email")
	labels["def"].append("Employee Phone Number")


        cur.execute("Select * from Employee")

        dic = { }
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

        return render_template('employeeTable.html', dic=dic, labels=labels, uName=uName)

#DeviceCategory table
@app.route('/deviceCategoryTable')
@login_required
@security_check
def deviceCategoryTable():
	uName = session['username']

        labels = { }
        labels.setdefault("def", [])
	labels["def"].append("Device Category ID")
        labels["def"].append("Device Category Name")
        labels["def"].append("Device Category  Description")

        cur.execute("Select * from DeviceCategory")
        dic = { }
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
                rowNum = rowNum + 1

        return render_template('deviceCategoryTable.html', dic=dic, labels=labels, uName=uName)



#taskType table
@app.route('/taskTypeTable')
@login_required
@security_check
def taskTypeTable():
	uName = session['username']

        labels = { }
        labels.setdefault("def", [])
        labels["def"].append("Task Type")
        labels["def"].append("Task Description")

        cur.execute("Select * from Task")

        dic = { }
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
                rowNum = rowNum + 1

        return render_template('taskTypeTable.html', dic=dic, labels=labels, uName=uName)

#deviceStatus table
@app.route('/deviceStatusTable')
@login_required
@security_check
def deviceStatusTable():
	uName = session['username']

        labels = { }
        labels.setdefault("def", [])
        labels["def"].append("Status ID")
        labels["def"].append("Status Description")

        cur.execute("Select * from DeviceStatus")

        dic = { }
        rowNum = 0
        for row in cur.fetchall():
                dic.setdefault(rowNum, [])
                dic[rowNum].append(row[0])
                dic[rowNum].append(row[1])
		dic[rowNum].append(row[2])
                rowNum = rowNum + 1

        return render_template('deviceStatusTable.html', dic=dic, labels=labels, uName=uName)

#admin task table
@app.route('/adminTaskTable')
@login_required
@security_check
def adminTaskTable():
	uName = session['username']
	
	labels = { }
        labels.setdefault("def", [])
        labels["def"].append("Task ID")
        labels["def"].append("Task Name")
        labels["def"].append("Task Location")
        labels["def"].append("Date Started")
        labels["def"].append("Date Completed")
        labels["def"].append("Task Status")
        labels["def"].append("Task Type")
        labels["def"].append("Active Task")
        labels["def"].append("Actual Completion Date")
        labels["def"].append("Device ID")
	labels["def"].append("User ID")
    
	dic = { }
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
                dic[rowNum].append(row[7])
                dic[rowNum].append(row[8])

		dID = "null"
                cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID = "+str(row[0]))
                for column in cur.fetchall():
                	dID = column[0]
                	dic[rowNum].append(column[0])
                cur.execute("SELECT User_UserID FROM User_has_Calendar WHERE Calendar_TaskID = "+str(row[0]))
                for column in cur.fetchall():
                        dID = column[0]
                	dic[rowNum].append(column[0])
                rowNum = rowNum + 1
        return render_template('taskTable.html', dic=dic, labels=labels, uName=uName)
		

#dropDownTestPage
#@app.route('/dropDownTestPage', methods=["GET", "POST"])
#@login_required
#def dropDownTestPage():
#	if request.method == 'POST':
#		taskType = request.form["taskType"]
#		return "taskType = "+taskType
#	else:
#		return render_template('dropDownTestPage.html')



#task table
#@app.route('/taskTable')
#@login_required
#def taskTable():
#	uID = session['userID']
#
#        labels = { }
#        labels.setdefault("def", [])
#        labels["def"].append("Task ID")
#        labels["def"].append("Date Started")
#        labels["def"].append("Date Completed")
#        labels["def"].append("Task Status")
#        labels["def"].append("Task Type")
#	labels["def"].append("Active Task")
#	labels["def"].append("Actual Completion Date")
#	labels["def"].append("Device ID")
#	labels["def"].append("Task Name")
#	labels["def"].append("Task Location")	
#	taskList = []
#
#        cur.execute("SELECT Calendar_TaskID FROM User_has_Calendar WHERE User_UserID = "+str(uID))
#	for row in cur.fetchall():
#		taskList.append(row[0])
#		
#	
#       dic = { }
#        rowNum = 0
#        for tasks in taskList:
#		taskCheck = rowNum
#		cur.execute("SELECT * FROM Calendar where TaskID = "+str(taskList[taskCheck]))
#		for row in cur.fetchall():
#			dic.setdefault(rowNum, [])
#                        dic[rowNum].append(row[0])
#                        dic[rowNum].append(row[1])
#                        dic[rowNum].append(row[2])
#                        dic[rowNum].append(row[3])
#                        dic[rowNum].append(row[4])
#	
#			if row[5] == 1:
#                                dic[rowNum].append("yes")
#                        else:
#                                dic[rowNum].append("no")
#                        dic[rowNum].append(row[6])
#			dic[rowNum].append(row[7])
#			dic[rowNum].append(row[8])
#                        dID = "null"
#                        cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID = "+str(row[0]))
#                        for column in cur.fetchall():
#				dID = column[0]
#                                dic[rowNum].append(column[0])
#			
#			
#                rowNum = rowNum + 1
#	return render_template('taskTable.html', dic=dic, labels=labels)



# search page
#@app.route('/search', methods=['GET', 'POST'])
#@login_required
#def search():
#	result = ""
#	taskID = None
#	userID = None
#	if request.method == 'POST':
#		if request.form['submit'] == 'Search Tasks':
#			taskID = request.form['TaskID']
#			cur.execute("SELECT User_UserID FROM User_has_Calendar WHERE Calendar_TaskID=\'"+taskID+"\'")
#			for column in cur.fetchall():
#				#converts values of column[0] to string
#				string = "%d" % column[0]
#				result = result+", "+string
#		elif request.form['submit'] == 'Search Users':
#			userID = request.form['UserID']
#			cur.execute("SELECT Calendar_TaskID FROM User_has_Calendar WHERE User_UserID=\'"+userID+"\'")
#			for column in cur.fetchall():
#				string = "d" % column[0]
#				result = result+", "+string
#		else:
#			result = 'Invalid entry.'

#	return render_template('search.html', result=result)

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    sec = 'null'
    error = None
    userType = None

    if 'logged_in' in session:
	return redirect(url_for('Inventory'))

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
#@app.route('/generic', methods=['GET', 'POST'])
#@login_required
#def generic():
        #if request.method == 'GET':
 #       taskID = request.args["id"]
  #      if request.method == 'POST':
   #             taskID = request.form["taskID"]
#                dateStart = request.form["dateStart"]
  #              dateComplete = request.form["dateComplete"]
   #             taskStatus = request.form["taskStatus"]
   #             taskType = request.form["taskType"]

 #               return "Request sucessfully submited!!"
  #      else:

   #             cur.execute("Select * from Calendar where TaskID = "+taskID)
#
  #              task  = { }
 #               task.setdefault("def", [])
    #            task["def"].append("Task ID")
   #             task["def"].append("Date Started")
     #           task["def"].append("Date Completed")
      #          task["def"].append("Task Status")
     #           task["def"].append("Task Type")

      #          rowNum = 0
       #         for row in cur.fetchall():
        #                task.setdefault(rowNum, [])
         #               task[rowNum].append(row[0])
          #              task[rowNum].append(row[1])
           #             task[rowNum].append(row[2])
            #            task[rowNum].append(row[3])
             #           task[rowNum].append(row[4])
              #          rowNum = rowNum + 1
              #  return render_template('generic.html', task=task)

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

                db.commit()

		cur.execute("UPDATE Phone SET PhoneNum = \'"+ePNumber+"\' WHERE Employee_EmployeeID = "+eID+" AND PhoneNum = "+str(empPhone))
               	
                db.commit()
                return redirect(url_for('employeeTable'))
	else:
		uName = session['username']
		eID = request.args["id"]
                emp = { }
                emp.setdefault("def", [])
                emp["def"].append("Employee ID")
                emp["def"].append("Employee Name")
                emp["def"].append("Job Title")
                emp["def"].append("Employee Address")
                emp["def"].append("Employee Department")
		emp["def"].append("Employee Email")
		emp["def"].append("Employee Phone Number")

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
		cur.execute("SELECT PhoneNum from Phone WHERE Employee_EmployeeID = "+eID+" LIMIT 1")
		for column in cur.fetchall():
			emp["data"].append(column[0])
		 	empPhone = column[0]
                return render_template('editEmployee.html', emp=emp, uName=uName)

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
		uName = session['username']
                emp = { }
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
          
                return render_template('editUser.html', emp=emp, uName=uName)

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
		uName = session['username']
               	emp = { }
                cur.execute("SELECT DateStart, DateComplete, TaskStatus, Task_TaskType, ActiveTask, DateActualCompletion, TaskName, TaskLocation, TaskID"
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
			emp["data"].append(row[8])
                cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID ="+tID)

		for row in cur.fetchall():
			emp["data"].append(row[0])
			devID = row[0] 
                
		rowNum = 0
	        device = { }
        	cur.execute("select DeviceID from Device")
        	for row in cur.fetchall():
                	device.setdefault(rowNum, [])
                	device[rowNum].append(row[0])
                	rowNum = rowNum + 1

        	rowNum = 0
        	task = { }
        	cur.execute("select TaskDesc from Task")
        	for row in cur.fetchall():
                	task.setdefault(rowNum, [])
                	task[rowNum].append(row[0])
                	rowNum = rowNum + 1

		
		return render_template('edittask.html', emp=emp, task = task, device = device, uName=uName)

#edit tasktype
@app.route('/edittasktype', methods=['GET', 'POST'])
@login_required
@security_check
def edittasktype():
	
        if request.method == "POST":
		ttID = request.args['id']
		tName = request.form["TaskName"]
                tDesc = request.form["TaskDesc"]
		testN = "null"
		testD = "null"
		cur.execute("SELECT TaskTypeName FROM Task WHERE TaskTypeName = \'"+tName+"\'")
		for row in cur.fetchall():
			testN = row[0]
                cur.execute("SELECT TaskDesc FROM Task WHERE TaskDesc = \'"+tDesc+"\'")
                for col in cur.fetchall():   
			testD = row[0]
		
		cur.execute("UPDATE Task SET TaskTypeName = \'"+tName+"\' WHERE TaskType = "+ttID)
                cur.execute("UPDATE Task SET TaskDesc = \'"+tDesc+"\' WHERE TaskType = "+ttID)
                db.commit()
                return redirect(url_for('taskTypeTable'))
	else:
                ttID = request.args['id']
		uName = session['username']
                emp = { }
             
                cur.execute("SELECT TaskTypeName, TaskDesc FROM Task WHERE TaskType = "+ttID)
           
                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
			emp["data"].append(row[1])
		emp["data"].append(ttID)                       
                return render_template('edittasktype.html', emp=emp, uName=uName)

#edit device category
@app.route('/editDeviceCategory', methods=['GET', 'POST'])
@login_required
@security_check
def editDeviceCategory():
        if request.method == "POST":
                dID = request.args['id']
                cDesc = request.form["CategoryDesc"]
		cName = request.form["CategoryName"]
                cur.execute("UPDATE DeviceCategory SET CategoryDesc = \'"+cDesc+"\' WHERE CategoryID = "+dID)
		cur.execute("UPDATE DeviceCategory SET CategoryName = \'"+cName+"\' WHERE CategoryID = "+dID)

                db.commit()
                return redirect(url_for('deviceCategoryTable'))
        else:
                dID = request.args['id']
		uName = session['username']
                emp = { }
                emp.setdefault("def", [])
                emp["def"].append("Device Category Name")
		emp["def"].append("Device Category Description")

                cur.execute("SELECT CategoryName, CategoryDesc FROM DeviceCategory WHERE CategoryID = "+dID)

                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
			emp["data"].append(row[1])
			emp["data"].append(dID)
                return render_template('editDeviceCategory.html', emp=emp, uName=uName)


#edit device status
@app.route('/editdevicestatus', methods=['GET', 'POST'])
@login_required	
@security_check
def editdevicestatus():
        if request.method == "POST":
		dID = request.args['id']
		sName = request.form["StatusName"]
                sDesc = request.form["StatusDesc"]
	
                cur.execute("UPDATE DeviceStatus SET StatusName = \'"+sName+"\' WHERE StatusID = "+dID)
		cur.execute("UPDATE DeviceStatus SET StatusDesc = \'"+sDesc+"\' WHERE StatusID = "+dID)
     
                db.commit()
                return redirect(url_for('deviceStatusTable'))
	else:
		dID = request.args['id']
		uName = session['username']
		emp = { }
		emp.setdefault("def", [])
                emp["def"].append("Status Name")
                emp["def"].append("Status Description")	
	
                cur.execute("SELECT StatusName, StatusDesc FROM DeviceStatus WHERE StatusID = "+dID)

                for row in cur.fetchall():
                        emp.setdefault("data", [])
                        emp["data"].append(row[0])
			emp["data"].append(row[1])
        		emp["data"].append(dID)    
                return render_template('editdevicestatus.html', emp=emp, uName=uName)


#user account page
@app.route('/myAccountPage')
@login_required
def account():
	# account dictionary for employee info
	account = {'uName': 'null', 'eName': 'null', 'role': 'null', 'email': 'null', 'address' : 'null', 'phone' : 'null'}
	eID = "null"
	eName = "null"
	userName = session['username']
	uName = session['username']
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
	active = { }
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
	
	

	return render_template('myAccountPage.html', account=account, active=active, deactive=deactive, uName=uName)
	  
#add employee
@app.route('/addemployee', methods=['GET', 'POST'])
@login_required
@security_check
def addemployee():
	uName = session['username']
	if request.method == "POST":
		
		eName = request.form["EmployeeName"]
		jTitle = request.form["JobTitle"]
		eAddress = request.form["EmployeeAddress"]
		ePNumber = request.form["EmployeePhoneNumber"]
		eDepartment = request.form["EmployeeDepartment"]
		email = request.form["EmployeeEmail"]
	    	
		emailCheck = "null"
		nCheck = "null"
		phnCheck = "null"
		
		cur.execute("SELECT EmployeeName FROM Employee WHERE EmployeeName = \'"+eName+"\'")
		for row in cur.fetchall():
			nCheck = row[0]
		
                cur.execute("SELECT EmployeeEmail FROM Employee WHERE EmployeeEmail = \'"+email+"\'")
                for row in cur.fetchall():
                        emailCheck = row[0]

                cur.execute("SELECT PhoneNum FROM Phone WHERE PhoneNum = \'"+ePNumber+"\'")
                for row in cur.fetchall():
			phnCheck = row[0]
		phnCheck = str(phnCheck)
		
		if(nCheck == eName):
			error = "Employee with that name already exists."
			return render_template('addemployee.html', error=error, uName=uName)
	
                if(emailCheck == email):
                        error = "Employee with that email address already exists."
                        return render_template('addemployee.html', error=error, uName=uName)

                if(phnCheck == str(ePNumber)):
                        error = "Employee with that phone number already exists."
                        return render_template('addemployee.html', error=error, uName=uName)

		else:
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
	
	uName = session['username']
	return render_template('addemployee.html', uName=uName)

#add user
@app.route('/adduser', methods=['GET', 'POST'])
@login_required
@security_check
def adduser():
	uName = session['username']
	if request.method == "POST":
		usName = request.form["UserName"]
		pWord = request.form["Password"]
		sec = request.form["Security"]
		eID = request.form["EmployeeID"]
		
		cur.execute("select EmployeeID from Employee where EmployeeName = \'"+eID+"\'")
         	for row in cur.fetchall():
			eID = row[0]
            	eID = str(eID)

		nCheck = "null"
		eCheck = 0
		cur.execute("SELECT UserName FROM User WHERE UserName = \'"+usName+"\'")
		for row in cur.fetchall():
			nCheck = row[0]
		
                cur.execute("SELECT Employee_EmployeeID FROM User WHERE Employee_EmployeeID = \'"+eID+"\'")
                for row in cur.fetchall():
                        eCheck = row[0]
		eCheck = str(eCheck)
	
		if(nCheck == usName):
			error = "Account with that username already exists."
			return render_template('adduser.html', error=error, uName=uName)

                elif(eCheck == eID):
                        error = "Account for selected employee already exists."
                        return render_template('adduser.html', error=error, uName=uName)
		
		else:
			cur.execute("INSERT INTO User (UserName, Password, Employee_EmployeeID, Security)"
				+" VALUES("
				+"\'"+usName+"\',"
				+"\'"+pWord+"\',"
				+"\'"+eID+"\',"
				+"\'"+sec+"\'"
				+")")
			db.commit()
			return redirect(url_for('userTable'))
	
	uName = session['username']
	rowNum = 0
        name = { }
        cur.execute("select EmployeeName from Employee")
        for row in cur.fetchall():
        	name.setdefault(rowNum, [])
        	name[rowNum].append(row[0])
        	rowNum = rowNum + 1
	
	return render_template('adduser.html', name = name, uName=uName)

#add task
@app.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
	uID = session['userID']
	uName = session['username']
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

		cur.execute("select TaskType from Task where TaskTypeName = \'"+tType+"\'")
		for row in cur.fetchall():
			tType = row[0]
		tType = str(tType)

                cur.execute("select DeviceID from Device where DeviceName = \'"+device+"\'")
                for row in cur.fetchall():
                        device = row[0]
                device = str(device)

		
		nCheck = "null"
	
		cur.execute("SELECT TaskName FROM Calendar WHERE TaskName = \'"+nTask+"\'")
		for row in cur.fetchall():
			nCheck = row[0]

		if(nCheck == nTask):
			error = "Task with that name already exists."
			return render_template('addtask.html', error=error, uName=uName)

		else:
	
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

			return redirect(url_for('calendar'))
	
	uName = session['username']
	rowNum = 0
        device = { }
        cur.execute("select DeviceName from Device")
        for row in cur.fetchall():
                device.setdefault(rowNum, [])
                device[rowNum].append(row[0])
                rowNum = rowNum + 1

	rowNum = 0
        task = { }
        cur.execute("select TaskTypeName from Task")
        for row in cur.fetchall():
                task.setdefault(rowNum, [])
                task[rowNum].append(row[0])
                rowNum = rowNum + 1

	return render_template('addtask.html', task = task, device = device, uName=uName)



#admin add task
@app.route('/adminaddtask', methods=['GET', 'POST'])
@login_required
@security_check
def adminaddtask():
	uName = session['username']
        if request.method == "POST":
                #taskID = request.form["TaskID"]
                taskID = 0
		username = request.form["UserName"]
                dStart = request.form["DateStarted"]
                dComp = request.form["DateCompleted"]
                tStatus = request.form["TaskStatus"]
                tType = request.form["TaskType"]
                acDate = "0000-00-00"
                device = request.form["DeviceID"]
                aTask = request.form["activeTask"]
                nTask = request.form["TaskName"]
                lTask = request.form["TaskLocation"]

                cur.execute("select TaskType from Task where TaskTypeName = \'"+tType+"\'")
                for row in cur.fetchall():
                        tType = row[0]
                tType = str(tType)

                cur.execute("select DeviceID from Device where DeviceName = \'"+device+"\'")
                for row in cur.fetchall():
                        device = row[0]
                device = str(device)

                cur.execute("select UserID from User where UserName = \'"+username+"\'")
                for row in cur.fetchall():
                        username = row[0]
                username = str(username)


                nCheck = "null"

                cur.execute("SELECT TaskName FROM Calendar WHERE TaskName = \'"+nTask+"\'")
                for row in cur.fetchall():
                        nCheck = row[0]

                if(nCheck == nTask):
                        error = "Task with that name already exists."
                        return render_template('adminaddtask.html', error=error, uName=uName)

                else:
          
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
                                +"\'"+username+"\',"
                                +"\'"+taskID+"\'"
                                +")")
                        db.commit()

                        cur.execute("INSERT INTO Device_has_Calendar (Device_DeviceID, Calendar_TaskID)"
                                +" VALUES("
                                +"\'"+device+"\',"
                                +"\'"+taskID+"\'"
                                +")")
                        db.commit()

                        return redirect(url_for('adminTaskTable'))

        uName = session['username']
        rowNum = 0
        device = { }
        cur.execute("select DeviceName from Device")
        for row in cur.fetchall():
                device.setdefault(rowNum, [])
                device[rowNum].append(row[0])
                rowNum = rowNum + 1

        rowNum = 0
        users = { }
        cur.execute("select UserName from User")
        for row in cur.fetchall():
                users.setdefault(rowNum, [])
                users[rowNum].append(row[0])
                rowNum = rowNum + 1

        rowNum = 0
        task = { }
        cur.execute("select TaskTypeName from Task")
        for row in cur.fetchall():
                task.setdefault(rowNum, [])
                task[rowNum].append(row[0])
                rowNum = rowNum + 1

        return render_template('adminaddtask.html', task = task, device = device, uName=uName, users=users)


#add taskType
@app.route('/addtasktype', methods=['GET', 'POST'])
@login_required
@security_check
def addtasktype():
	uName = session['username']
	if request.method == "POST":
		tName = request.form["TaskName"]
		tDesc = request.form["TaskDesc"]
		testN = "null"
		testD = "null"
		cur.execute("SELECT TaskTypeName FROM Task WHERE TaskTypeName = \'"+tName+"\'")
		for row in cur.fetchall():
			testN = row[0]
		cur.execute("SELECT TaskDesc FROM Task WHERE TaskDesc = \'"+tDesc+"\'")
		for col in cur.fetchall():
			testD = col[0]
		if(testN == tName): 

                        error = "Task type with that name already exists."
                        return render_template('addtasktype.html', error=error, uName=uName)

		elif(testD == tDesc):

			error = "Task type with that description already exists"
                        return render_template('addtasktype.html', error=error, uName=uName)
		else:

			cur.execute("INSERT INTO Task (TaskTypeName, TaskDesc)"
					+" VALUES("
					+"\'"+tName+"\',"
					+"\'"+tDesc+"\'"
					+")")
			db.commit()
			return redirect(url_for('taskTypeTable'))
	
	uName = session['username']
	return render_template('addtasktype.html', uName=uName)

#add deviceStatus
@app.route('/adddevicestatus', methods=['GET', 'POST'])
@login_required
@security_check
def adddevicestatus():
	uName = session['username']
	if request.method == "POST":
		sName = request.form["StatusName"]
                sDesc = request.form["StatusDesc"]
		
		nCheck = "null"
		dCheck = "null"

		cur.execute("SELECT StatusName FROM DeviceStatus WHERE StatusName = \'"+sName+"\'")
		for row in cur.fetchall():
			nCheck = row[0]
		
                cur.execute("SELECT StatusDesc FROM DeviceStatus WHERE StatusDesc = \'"+sDesc+"\'")
                for row in cur.fetchall():
                        dCheck = row[0]

		if(nCheck == sName):
			error = "Device status with that name already exists."
			return render_template('adddevicestatus.html', error=error, uName=uName)

                elif(dCheck == sDesc):
                        error = "Device status with that description already exists."
                        return render_template('adddevicestatus.html', error=error, uName=uName)


		else:
               		cur.execute("INSERT INTO DeviceStatus (StatusName, StatusDesc)"
                                +" VALUES("
                                +"\'"+sName+"\'"
                                +",\'"+sDesc+"\'"
                                +")")
                	db.commit()
                	return redirect(url_for('deviceStatusTable'))
	
	uName = session['username']
        return render_template('adddevicestatus.html', uName=uName)
	
		
#add deviceCategory
@app.route('/addDeviceCategory', methods=['GET', 'POST'])
@login_required
@security_check
def addDeviceCategory():
	uName = session['username']
        if request.method == "POST":
                cDesc = request.form["CategoryDesc"]
		cName = request.form["CategoryName"]
		
		nCheck = "null"
		dCheck = "null"

		cur.execute("SELECT CategoryName from DeviceCategory WHERE CategoryName = \'"+cName+"\'")
		for row in cur.fetchall():
			nCheck = row[0]
		
                cur.execute("SELECT CategoryDesc from DeviceCategory WHERE CategoryDesc = \'"+cDesc+"\'")
                for row in cur.fetchall():
                        dCheck = row[0]

		if(nCheck == cName):
			error = "Device category with that name already exists."
			return render_template('addDeviceCategory.html', error=error, uName=uName)
              
		elif(dCheck == cDesc):
                        error = "Device category with that description already exists."
                        return render_template('addDeviceCategory.html', error=error, uName=uName)

		else:
                	cur.execute("INSERT INTO DeviceCategory (CategoryDesc, CategoryName)"
                                +" VALUES("
                                +"\'"+cDesc+"\'"
				+",\'"+cName+"\'"
                                +")")
                	db.commit()
                	return redirect(url_for('deviceCategoryTable'))

	uName = session['username']
        return render_template('addDeviceCategory.html', uName=uName)

#new device page
@app.route('/addDevice', methods=["GET", "POST"])
@login_required
def addDevice():
	uName = session['username']
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

		nCheck = "null"
		serCheck = "null"
		strSerNum = str(sNumber)

		cur.execute("select StatusID from DeviceStatus where StatusDesc = \'"+deviceStatus+"\'")
		for row in cur.fetchall():
			deviceStatus = row[0]
		deviceStatus = str(deviceStatus)

		cur.execute("select CategoryID from DeviceCategory where CategoryName = \'"+deviceCategory+"\'")
                for row in cur.fetchall():
                        deviceCategory = row[0]
                deviceCategory = str(deviceCategory)

		cur.execute("SELECT DeviceName from Device WHERE DeviceName = \'"+deviceName+"\'")
		for col in cur.fetchall():
			nCheck = col[0]
		
                cur.execute("SELECT SerialNumber from Device WHERE SerialNumber = \'"+sNumber+"\'")
                for col in cur.fetchall():
                        serCheck = col[0]
		
		if(nCheck == deviceName):
			error = "Device with that name already exists."
			return render_template('addDevice.html', error=error, uName=uName)
		
		elif(serCheck == strSerNum):
			error = "Device with that serial number already exists."
			return render_template('addDevice.html', error=error, uName=uName)
		
		else:
			cur.execute("INSERT INTO Device (DeviceName, Description, DeviceCategory_CategoryID, DeviceStatus_StatusID, DeviceLocation, DeviceOwner, DateOfDeployment, GoBackDate, IPAddress, SerialNumber)"
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
	
	uName = session['username']
	rowNum = 0
	dStatusL = { }
	cur.execute("select StatusDesc from DeviceStatus")
	for row in cur.fetchall():
		dStatusL.setdefault(rowNum, [])
		dStatusL[rowNum].append(row[0])
		rowNum = rowNum + 1
	num = 0
        cat = { }
        cur.execute("select CategoryName from DeviceCategory")
        for row in cur.fetchall():
        	cat.setdefault(num, [])
        	cat[num].append(row[0])
        	num = num + 1
		
	return render_template('addDevice.html', dStatusL = dStatusL, cat=cat, uName=uName)		

#edit account
#@app.route('/editAccount', methods=['GET', 'POST'])
#@login_required
#def editAccount():
#        account = {'uName': 'null',  'fName': 'John', 'lName': 'null', 'role': 'null', 'email': 'null'}
#        eID = "null"
#        eName = "null"
#        userName = session['username']
#        cur.execute("Select UserName, EmployeeID from User where UserName = "+userName)
#        for column in cur.fetchall():
#                account['uName'] = column[0]
#                eID = column[1]
#        cur.execute("Select EmployeeName, JobTitle, EmployeeEmail from Employee where EmployeeID = "+eID)
#        for column in cur.fetchall():
#                eName = column[0]
#                account['role'] = column[1]
#                account['email'] = column[2]
#        eNameS = eName.split(" ")
#        fName = eNameS[0]
#        lName = eNameS[1]
#        account['fName'] = fName
#        account['lName'] = lName
#	if request.method == 'POST':
#		account['fName'] = request.form("fName")
#		account['lName'] = request.form("lname")
#		account['role'] = request.form("role")
#		account['email'] = request.form("email")
#		firstName = account['fName']
#		lastName = account['lName']
#		role = account['role']
#		email = account['email']
#		fullName = firstName + " " + lastName
#		cur.execute("Update Employee "
#				+ "set EmployeeName = \'"+fullName+"\',"
#				+ " JobtTitle = \'" +role+"\',"
#				+ " EmployeeEmail = \'"+email+"\' where EmployeeID = \'"+eID+"\'")
#		db.commit()
#		return redirect(url_for('account'))
#	
#	return render_template('editAccount.html', account=account)

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

	uName = session['username']
	cur.execute("SELECT EmployeeName from Employee")
	emp = {}
	for row in cur.fetchall():
		emp.setdefault(row, "")
		emp[row] = row[0]	
	return render_template('deleteemployee.html', emp = emp, uName=uName)

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

	uName = session['username']
	cur.execute("select UserName from User")
	user = {}
	for row in cur.fetchall():
		user.setdefault(row, "")
		user[row] = row[0]
        return render_template('deleteuser.html', user = user, uName=uName)

#regular delete Calendar Task
@app.route('/deleteCalendarTask', methods=['GET', 'POST'])
@login_required
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
                return redirect(url_for('calendar'))
	
	username = session['username']
	uName = session['username']
	
	cur.execute("select TaskName from Calendar, User_has_Calendar, User where User_UserID = UserID and TaskID = Calendar_TaskID and UserName = \'"+username+"\'") 	
	#cur.execute("SELECT TaskName from Calendar")
	taskList = {}
	for row in cur.fetchall():
		taskList.setdefault(row, "")
		taskList[row] = row[0]
	
        return render_template('deleteCalendarTask.html', taskList = taskList, uName=uName)

#admin delete Calendar Task
@app.route('/admindeleteCalendarTask', methods=['GET', 'POST'])
@login_required
@security_check
def admindeleteCalendarTask():
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
                return redirect(url_for('adminTaskTable'))

        username = session['username']
        uName = session['username']

        #cur.execute("select TaskName from Calendar, User_has_Calendar, User where User_UserID = UserID and TaskID$
        cur.execute("SELECT TaskName from Calendar")
        taskList = {}
        for row in cur.fetchall():
                taskList.setdefault(row, "")
                taskList[row] = row[0]

        return render_template('deleteCalendarTask.html', taskList = taskList, uName=uName)


#delete device
@app.route('/deleteDevice', methods=['GET', 'POST'])
@login_required
@security_check
def deleteDevice():
        if request.method == 'POST':
		sNumber = request.form["SerialNumber"]
		cur.execute("SELECT DeviceID from Device WHERE DeviceName = "+str(sNumber))
		for row in cur.fetchall():
			dID = row[0]

		#dID = request.form["deviceID"]
		dID = str(dID)
		cur.execute("DELETE FROM Device_has_Calendar WHERE Device_deviceID = "+dID)
                cur.execute("DELETE FROM Device WHERE deviceID = "+dID)
                db.commit()
		return redirect(url_for('Inventory'))

	uName = session['username']
	device = {}
	cur.execute("SELECT DeviceName from Device")
	for row in cur.fetchall():
		device.setdefault(row, "")
		device[row] = row[0]

        return render_template('deleteDevice.html', device = device, uName=uName)
#delete deviceCategory
@app.route('/deleteDeviceCategory', methods=['GET', 'POST'])
@login_required
@security_check
def deleteDeviceCategory():
        if request.method == 'POST':
                cName = request.form["DeviceCategory"]
                cur.execute("SELECT CategoryID from DeviceCategory WHERE CategoryName = \'"+cName+"\'")
                sID = 0
                for row in cur.fetchall():
                        sID = row[0]
		cur.execute("UPDATE Device SET DeviceCategory_CategoryID = NULL WHERE DeviceCategory_CategoryID = \'"+str(sID)+"\'")
                cur.execute("DELETE FROM DeviceCategory WHERE CategoryID = "+str(sID))
                db.commit()
                return redirect(url_for('deviceCategoryTable'))

	uName = session['username']

        cur.execute("SELECT CategoryName from DeviceCategory")
        category = {}
        for row in cur.fetchall():
                category.setdefault(row, "")
                category[row] = row[0]

        return render_template('deleteDeviceCategory.html', category = category, uName=uName)


#delete deviceStatus
@app.route('/deleteDeviceStatus', methods=['GET', 'POST'])
@login_required
@security_check
def deleteDeviceStatus():
        if request.method == 'POST':
		status = request.form["DeviceStatus"]
		cur.execute("SELECT StatusID from DeviceStatus WHERE StatusName = \'"+status+"\'")
		sID = 0
		for row in cur.fetchall():
			sID = row[0]
		cur.execute("UPDATE Device SET DeviceStatus_StatusID = NULL WHERE DeviceStatus_StatusID = \'"+str(sID)+"\'")
                cur.execute("DELETE FROM DeviceStatus WHERE StatusID = "+str(sID))
                db.commit()
                return redirect(url_for('deviceStatusTable'))
	
	uName = session['username']
	cur.execute("SELECT StatusName from DeviceStatus")
	dStatus = {}
	for row in cur.fetchall():
		dStatus.setdefault(row, "")
		dStatus[row] = row[0]

        return render_template('deleteDeviceStatus.html', dStatus = dStatus, uName=uName)

#delete TaskType
@app.route('/deleteTaskType', methods=['GET', 'POST'])
@login_required
@security_check
def deleteTaskType():
        if request.method == 'POST':
		tName = request.form["TaskDesc"]
		sID = 0
                #tID = request.form["taskType"]
		cur.execute("SELECT TaskType FROM Task WHERE TaskTypeName = \'"+tName+"\'")
		for row in cur.fetchall():
			sID = row[0]
		cur.execute("UPDATE Calendar SET Task_TaskType = NULL WHERE Task_TaskType - \'"+str(sID)+"\'")  
                cur.execute("DELETE FROM Task WHERE TaskType = \'"+str(sID)+"\'")
                db.commit()
                return redirect(url_for('taskTypeTable'))

	uName = session['username']
	cur.execute("SELECT TaskTypeName from Task")
	task = {}
	for row in cur.fetchall():
		task.setdefault(row, "")
		task[row] = row[0]
        return render_template('deleteTaskType.html', task = task, uName=uName)
 			
#change password
@app.route('/editPassword', methods=['GET', 'POST'])
@login_required
def editPassword():
	pWord = "null"
	pCheck = "null"
	username = session['username']
	uName = session['username']
	if request.method == 'POST':
		opWord = request.form["OldPassword"]
		pWord = request.form["NewPassword"]
		rpWord = request.form["RetypePassword"]
	
		cur.execute("Select Password from User where UserName = \'"+username+"\'")
		for row in cur.fetchall():
			pCheck = row[0]
		if(opWord == pCheck):	
			if(pWord == rpWord):
				print("test")
				cur.execute("Update User set Password = \'" + pWord + "\' where UserName = \'"+username+"\'")
				db.commit()
				return redirect(url_for('account'))
			else:
				error2 = "New passwords do not match."
				return render_template('editPassword.html', error2=error2, uName=uName)
		else:
			error1 = "Old Password does not match "
			return render_template('editPassword.html', error1=error1, uName=uName)
				
	return render_template('editPassword.html', uName=uName)

#userPage
@app.route('/userPage', methods=['GET', 'POST'])
@login_required
@security_check
def userPage():
	uName = session['username']
	return render_template('userPage.html', uName=uName)




#Calendar
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
	dev = 0
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
		cur.execute("Select Device_DeviceID from Device_has_Calendar WHERE Calendar_TaskID = \'"+str(row[0])+"\'")
		if cur.rowcount == 0:
			dev = 0
		else:
			for col in cur.fetchall():	
				dev = col[0]
		cur.execute("select SerialNumber from Device where DeviceID = \'"+str(dev)+"\'")
		for col in cur.fetchall():	
			dic[rowNum].append(col[0])
                rowNum = rowNum + 1
			
	cur.execute("select TaskID, DateComplete, TaskDesc, TaskStatus, TaskName, TaskLocation from Calendar, Task "
                        +"where Calendar.Task_TaskType = Task.TaskType and DateComplete != '0000-00-00'")
        dic2 = { }
        num = 0
	devID = 0
        for column in cur.fetchall():
                dic2.setdefault(num, [])
                dic2[num].append(column[0])
                dic2[num].append(column[1])
                dic2[num].append(column[2])
                dic2[num].append(column[3])
		dic2[num].append(column[4])
                dic2[num].append(column[5])
		cur.execute("Select Device_DeviceID from Device_has_Calendar WHERE Calendar_TaskID = \'"+str(column[0])+"\'")
                if cur.rowcount == 0:
                        devID = 0
                else:
			for col in cur.fetchall():
                       		devID = col[0]
                cur.execute("select SerialNumber from Device where DeviceID = \'"+str(devID)+"\'")
		for rows in cur.fetchall():
                        dic2[num].append(rows[0])
		num = num + 1
	
	uName = session['username']
        return render_template('calendar.html', dic=dic, dic2=dic2, uName=uName)

@app.route("/_edit_device")
def edit_device():
	deviceID = request.args.get("id")
	dLocation = request.args.get("DeviceLocation")
        sNumber = request.args.get("SerialNumber")
        deviceName = request.args.get("DeviceName")
        IP = request.args.get("IPAddress")
        IPInt = int(IP)
        owner = request.args.get("DeviceOwner")
        desc = request.args.get("Description")
        DoD = request.args.get("DateOfDeployment")
        go_back = request.args.get("GoBackDate")
        deviceCategory = request.args.get("DeviceCategory")
        deviceStatus = request.args.get("deviceStatus")
	testS = "NULL"
	testN = "null"
	OldName = "null"
	OldSerial = "null"
	try:
		cur.execute("SELECT DeviceName FROM Device WHERE DeviceID = \'"+deviceID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != deviceName):
                        cur.execute("SELECT DeviceName FROM Device WHERE DeviceName = \'"+deviceName+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == deviceName):
                                return jsonify(result="Device with that name already exists.")

		cur.execute("SELECT SerialNumber FROM Device WHERE DeviceID = \'"+deviceID+"\'")
                for row in cur.fetchall():
                        OldSerial = row[0]
                if(OldSerial != sNumber):
                        cur.execute("SELECT SerialNumber FROM Device WHERE SerialNumber = \'"+sNumber+"\'")
                        for row in cur.fetchall():
                                testS = row[0]
                        if(testS == sNumber):
                                return jsonify(result="Device with that serial number already exists.")
		
	  	cur.execute("select StatusID from DeviceStatus where StatusName = \'"+deviceStatus+"\'")
            	for row in cur.fetchall():
                	deviceStatus = row[0]
            	deviceStatus = str(deviceStatus)

            	cur.execute("select CategoryID from DeviceCategory where CategoryName = \'"+deviceCategory+"\'")
            	for row in cur.fetchall():
                	deviceCategory = row[0]
            	deviceCategory = str(deviceCategory)
		cur.execute("UPDATE Device SET DeviceName = \'"+deviceName+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET Description = \'"+desc+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET DeviceCategory_CategoryID = \'"+deviceCategory+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET DeviceStatus_StatusID = \'"+deviceStatus+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET DeviceLocation = \'"+dLocation+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET DeviceOwner = \'"+owner+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET DateOfDeployment = \'"+DoD+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET GoBackDate = \'"+go_back+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET IPAddress = \'"+IP+"\' WHERE DeviceID = "+deviceID)
            	cur.execute("UPDATE Device SET SerialNumber = \'"+sNumber+"\' WHERE DeviceID = "+deviceID)
		db.commit()
		return jsonify(result="Successful")

        except MySQLdb.IntegrityError:
                return jsonify(result="Failed")


@app.route("/_edit_employee")
def edit_employee():
	eID = request.args.get("id")
	eName = request.args.get("EmployeeName")
	jTitle = request.args.get("JobTitle")
	eAddress = request.args.get("EmployeeAddress")
	ePNumber = request.args.get("EmployeePhoneNumber")
	eDepartment = request.args.get("EmployeeDepartment")
	email = request.args.get("EmployeeEmail")
	testN = "null"
	testP = "null"
	testE = "null"
        OldName = "null"
	OldEmail = "null"
	OldPhone = "null"
	try:
		cur.execute("SELECT EmployeeName FROM Employee WHERE EmployeeID = \'"+eID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != eName):
                        cur.execute("SELECT EmployeeName FROM Employee WHERE EmployeeName = \'"+eName+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == eName):
                                return jsonify(result="Employee with that name already exists.")
		
		cur.execute("SELECT EmployeeEmail FROM Employee WHERE EmployeeID = \'"+eID+"\'")
                for row in cur.fetchall():
                        OldEmail = row[0]
		if(OldEmail != email):
                        cur.execute("SELECT EmployeeEmail FROM Employee WHERE EmployeeEmail = \'"+email+"\'")
                        for row in cur.fetchall():
                                testE = row[0]
                        if(testE == email):
                                return jsonify(result="Employee with that email address already exists.")

		cur.execute("SELECT PhoneNum FROM Phone WHERE Employee_EmployeeID = \'"+eID+"\'")
                for row in cur.fetchall():
                        OldPhone = row[0]
                if(OldPhone != ePNumber):
                        cur.execute("SELECT PhoneNum FROM Phone WHERE PhoneNum = \'"+ePNumber+"\'")
                        for row in cur.fetchall():
                                testP = row[0]
                        if(testP == ePNumber):
                                return jsonify(result="Employee with that phone number already exists.")

		cur.execute("UPDATE Employee SET EmployeeName = \'"+eName+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET JobTitle = \'"+jTitle+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeAddress = \'"+eAddress+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeDepartment = \'"+eDepartment+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Employee SET EmployeeEmail = \'"+email+"\' WHERE EmployeeID = "+eID)
		cur.execute("UPDATE Phone SET PhoneNum = \'"+ePNumber+"\' WHERE Employee_EmployeeID = "+eID)
		db.commit()
		return jsonify(result="Successful")

        except MySQLdb.IntegrityError:
                return jsonify(result="Failed")

@app.route("/_edit_user")
def edit_user():
	ID = request.args.get("id")
	Name = request.args.get("UserName")
	Word = request.args.get("Password")
	sec = request.args.get("Security")
	testN = "null"
	OldName = "null"
#	ID = ID[1:-1]
	try:
        	cur.execute("SELECT UserName FROM User WHERE UserID = \'"+ID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != Name):
                        cur.execute("SELECT UserName FROM User WHERE UserName = \'"+Name+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == Name):
                                return jsonify(result="UserName with that name already exists.")
			
		cur.execute("UPDATE User SET UserName = \'"+Name+"\' WHERE UserID = "+ID)
		cur.execute("UPDATE User SET Password = \'"+Word+"\' WHERE UserID = "+ID)
		cur.execute("UPDATE User SET Security = \'"+sec+"\' WHERE UserID = "+ID)
		db.commit()
                return jsonify(result="Successful")

        except MySQLdb.IntegrityError:
                return jsonify(result="Failed")



@app.route("/_edit_device_category")
def edit_device_category():
	ID = request.args.get('id')
	Desc = request.args.get("CategoryDesc")
	Name = request.args.get("CategoryName")
	testN = "null"
        testD = "null"
        OldName = "null"
        OldDesc = "null"
        ID = ID[1:-1]
	try:
		cur.execute("SELECT CategoryName FROM DeviceCategory WHERE CategoryID = \'"+ID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != Name):
                        cur.execute("SELECT CategoryName FROM DeviceCategory WHERE CategoryName = \'"+Name+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == Name):
                                return jsonify(result="Category Name with that name already exists.")

		cur.execute("SELECT CategoryDesc FROM DeviceCategory WHERE CategoryID = \'"+ID+"\'")
                for row in cur.fetchall():
                        OldDesc = row[0]

                if(OldDesc != Desc):
                        cur.execute("SELECT CategoryDesc FROM DeviceCategory WHERE CategoryDesc = \'"+Desc+"\'")
                        for col in cur.fetchall():
                                testD = col[0]
                        if(testD == Desc):
                                return jsonify(result="Category Description already exists.")

                cur.execute("UPDATE DeviceCategory SET CategoryName = \'"+Name+"\' WHERE CategoryID = "+ID)
                cur.execute("UPDATE DeviceCategory SET CategoryDesc = \'"+Desc+"\' WHERE CategoryID = "+ID)
                db.commit()
                return jsonify(result="Successful")

        except MySQLdb.IntegrityError:
                return jsonify(result="Failed")




@app.route("/_edit_device_status")
def edit_device_status():
	ID = request.args.get('id')
	Name = request.args.get("StatusName")
	Desc = request.args.get("StatusDesc")
	testN = "null"
        testD = "null"
        OldName = "null"
        OldDesc = "null"
        ID = ID[1:-1]
	try:
		cur.execute("SELECT StatusName FROM DeviceStatus WHERE StatusID = \'"+ID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != Name):
                        cur.execute("SELECT StatusName FROM DeviceStatus WHERE StatusName = \'"+Name+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == Name):
                                return jsonify(result="Status Name with that name already exists.")

                cur.execute("SELECT StatusDesc FROM DeviceStatus WHERE StatusID = \'"+ID+"\'")
                for row in cur.fetchall():
                        OldDesc = row[0]

                if(OldDesc != Desc):
                        cur.execute("SELECT StatusDesc FROM DeviceStatus WHERE StatusDesc = \'"+Desc+"\'")
                        for col in cur.fetchall():
                                testD = col[0]
                        if(testD == Desc):
                                return jsonify(result="Status Description already exists.")

		cur.execute("UPDATE DeviceStatus SET StatusName = \'"+Name+"\' WHERE StatusID = "+ID)
                cur.execute("UPDATE DeviceStatus SET StatusDesc = \'"+Desc+"\' WHERE StatusID = "+ID)
                db.commit()
                return jsonify(result="Successful")

	except MySQLdb.IntegrityError:
                return jsonify(result="Failed")


@app.route("/_edit_task")
def edit_task():
	
	tID = request.args.get('id')
	nTask = request.args.get("TaskName")
        lTask = request.args.get("TaskLocation")
        dStart = request.args.get("DateStarted")
        dComp = request.args.get("DateCompleted")
        tStatus = request.args.get("TaskStatus")
        tType = request.args.get("TaskType")
        aTask = request.args.get("ActiveTask")
        acDate = request.args.get("ActualCompletionDate")
        device = request.args.get("DeviceID")
	testN = "null"
	OldName = "null"
	devID = 0
			
	cur.execute("SELECT Device_DeviceID FROM Device_has_Calendar WHERE Calendar_TaskID ="+tID)
	for row in cur.fetchall():
        	devID = row[0]

        cur.execute("select TaskType from Task where TaskDesc = \'"+tType+"\'")
        for row in cur.fetchall():
        	tType  = row[0]
        tType = str(tType)
	
	try:
		cur.execute("SELECT TaskName FROM Calendar WHERE TaskID = \'"+tID+"\'")
                for row in cur.fetchall():
                        OldName = row[0]
                if(OldName != nTask):
                        cur.execute("SELECT TaskName FROM Calendar WHERE TaskName = \'"+nTask+"\'")
                        for row in cur.fetchall():
                                testN = row[0]
                        if(testN == nTask):
                                return jsonify(result="Task Type with that name already exists.")
		print("task active: "+aTask)	
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
		return jsonify(result="Successful")

        except MySQLdb.IntegrityError:
                return jsonify(result="Failed")
	
	

@app.route("/_edit_task_type")
def edit_task_type():
	ttID = request.args.get('id')
        tName = request.args.get("TaskName")
        tDesc = request.args.get("TaskDesc")
        testN = "null"
        testD = "null"
	tOldName = "null"
	tOldDesc = "null"
	ttID = ttID[1:-1]	
	try:
		cur.execute("SELECT TaskTypeName FROM Task WHERE TaskType = \'"+ttID+"\'")
		for row in cur.fetchall():
			tOldName = row[0]
		if(tOldName != tName):
			cur.execute("SELECT TaskTypeName FROM Task WHERE TaskTypeName = \'"+tName+"\'")
			for row in cur.fetchall():
                       		testN = row[0]
			if(testN == tName):
				print("inside")
				return jsonify(result="Task Type with that name already exists.")
					
		cur.execute("SELECT TaskDesc FROM Task WHERE TaskType = \'"+ttID+"\'")
		for row in cur.fetchall():
			tOldDesc = row[0]
		
		if(tOldDesc != tDesc):		
			cur.execute("SELECT TaskDesc FROM Task WHERE TaskDesc = \'"+tDesc+"\'")
			for col in cur.fetchall():
                       		testD = col[0]
			if(testD == tDesc):
				return jsonify(result="Task Description already exists.")
						
		cur.execute("UPDATE Task SET TaskTypeName = \'"+tName+"\' WHERE TaskType = "+ttID)
		cur.execute("UPDATE Task SET TaskDesc = \'"+tDesc+"\' WHERE TaskType = "+ttID)
		db.commit()
		return jsonify(result="Successful")
	
	except MySQLdb.IntegrityError:
		return jsonify(result="Failed")
	
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded = True, debug = False)
