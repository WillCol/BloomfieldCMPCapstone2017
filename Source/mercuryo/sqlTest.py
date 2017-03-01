 #!/user/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="Inventory")
cur = db.cursor()

taskID = '1'

cur.execute("SELECT User_UserID FROM User_has_Calendar WHERE Calendar_TaskID = "+taskID)
result = ''
for column in cur.fetchall():
	h1 = "%d" % column[0]
	result = result + h1 + ", "
print result	
db.close()
