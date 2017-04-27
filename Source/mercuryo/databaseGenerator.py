#!/bin/python
# python program
import MySQLdb as db
import sys

con = db.connect(user="root",passwd="root")
cur = con.cursor()

dbUser = raw_input("Input MySQL Username: ")
dbPW = raw_input("Input MySQL Password: ")
dName = raw_input("Input Database Name: ")
sys.stdout = open('dbconfig.txt', 'w')
print dName
print dbUser
print dbPW
sys.stdout.close()

cur.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
cur.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
cur.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';")

cur.execute('CREATE SCHEMA IF NOT EXISTS '+dName+' DEFAULT CHARACTER SET utf8;')
#cur.execute('CREATE SCHEMA IF NOT EXISTS `mrcInventory` DEFAULT CHARACTER SET utf8;')


con = db.connect(host="localhost",user="root",passwd="root",db=dName)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Task`"
	+" (`TaskType` INT(11) NOT NULL AUTO_INCREMENT, `TaskTypeName` VARCHAR(45) NOT NULL, `TaskDesc` VARCHAR(45) NOT NULL, PRIMARY KEY (`TaskType`),"
  	+" UNIQUE INDEX `TaskDesc_UNIQUE` (`TaskDesc` ASC),"
  	+" UNIQUE INDEX `TaskType_UNIQUE` (`TaskType` ASC),"
        +" UNIQUE INDEX `TaskTypeName_UNIQUE` (`TaskTypeName` ASC))"
	+" ENGINE = InnoDB"
	+" AUTO_INCREMENT = 1"
	+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Calendar` ("
  +" `TaskID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `DateStart` DATE NOT NULL,"
  +" `DateComplete` DATE NULL DEFAULT NULL,"
  +" `TaskStatus` VARCHAR(45) NOT NULL,"
  +" `Task_TaskType` INT(11) NOT NULL,"
  +" `ActiveTask` INT(1) NOT NULL DEFAULT '1',"
  +" `DateActualCompletion` DATE NULL DEFAULT NULL,"
  +" `TaskName` VARCHAR(45) BINARY NULL DEFAULT NULL,"
  +" `TaskLocation` VARCHAR(45) NULL DEFAULT NULL,"
  +" PRIMARY KEY (`TaskID`),"
  +" UNIQUE INDEX `TaskID_UNIQUE` (`TaskID` ASC),"
  +" UNIQUE INDEX `TaskName_UNIQUE` (`TaskName` ASC),"
  +" INDEX `fk_Calendar_Task1_idx` (`Task_TaskType` ASC),"
  +" CONSTRAINT `fk_Calendar_Task1`"
   +"  FOREIGN KEY (`Task_TaskType`)"
   +" REFERENCES "+dName+".`Task` (`TaskType`)"
   +" ON DELETE NO ACTION"
   +" ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 1"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`DeviceCategory` ("
  +"`CategoryID` INT(11) NOT NULL AUTO_INCREMENT,"
  +"`CategoryName` VARCHAR(64) NULL DEFAULT NULL,"
  +"`CategoryDesc` VARCHAR(64) NULL DEFAULT NULL,"
  +" PRIMARY KEY (`CategoryID`),"
  +" UNIQUE INDEX `CategoryID_UNIQUE` (`CategoryID` ASC),"
  +" UNIQUE INDEX `CategoryName_UNIQUE` (`CategoryName` ASC),"
  +" UNIQUE INDEX `CategoryDesc_UNIQUE` (`CategoryDesc` ASC))"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 1"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`DeviceStatus` ("
  +" `StatusID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `StatusName` VARCHAR(64) NOT NULL,"
  +" `StatusDesc` VARCHAR(45) NOT NULL,"
  +" PRIMARY KEY (`StatusID`),"
  +" UNIQUE INDEX `StatusID_UNIQUE` (`StatusID` ASC),"
  +" UNIQUE INDEX `StatusName_UNIQUE` (`StatusName` ASC),"
  +" UNIQUE INDEX `StatusDesc_UNIQUE` (`StatusDesc` ASC))"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 1"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Device` ("
  +" `DeviceID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `DeviceName` VARCHAR(25) NOT NULL,"
  +" `Description` VARCHAR(45) NULL DEFAULT NULL,"
  +" `DeviceCategory_CategoryID` INT(11) NULL DEFAULT NULL,"
  +" `DeviceStatus_StatusID` INT(11) NULL DEFAULT NULL,"
  +" `DeviceLocation` VARCHAR(45) NOT NULL,"
  +" `DeviceOwner` VARCHAR(45) NULL DEFAULT NULL ,"
  +" `DateOfDeployment` DATE NULL DEFAULT NULL,"
  +" `GoBackDate` DATE NULL DEFAULT NULL,"
  +" `IPAddress` VARCHAR(16) NULL DEFAULT NULL,"
  +" `SerialNumber` VARCHAR(30) NULL DEFAULT NULL,"
  +" PRIMARY KEY (`DeviceID`),"
  +" UNIQUE INDEX `DeviceID_UNIQUE` (`DeviceID` ASC),"
  +" UNIQUE INDEX `DeviceName_UNIQUE` (`DeviceName` ASC),"
  +" UNIQUE INDEX `SerialNumber_UNIQUE` (`SerialNumber` ASC),"
  +" INDEX `fk_Device_DeviceStatus1_idx` (`DeviceStatus_StatusID` ASC),"
  +" INDEX `fk_DeviceCategory_CategoryID_idx` (`DeviceCategory_CategoryID` ASC),"
  +" CONSTRAINT `fk_DeviceCategory_CategoryID`"
  +" FOREIGN KEY (`DeviceCategory_CategoryID`)"
  +" REFERENCES "+dName+".`DeviceCategory` (`CategoryID`)"
  +" ON DELETE NO ACTION"
  +" ON UPDATE NO ACTION,"
  +" CONSTRAINT `fk_Device_DeviceStatus1`"
  +" FOREIGN KEY (`DeviceStatus_StatusID`)"
  +" REFERENCES "+dName+".`DeviceStatus` (`StatusID`)"
  +" ON DELETE NO ACTION"
  +" ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 1"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Device_has_Calendar` ("
+"  `Device_DeviceID` INT(11) NULL DEFAULT '0',"
+"  `Calendar_TaskID` INT(11) NULL DEFAULT '0',"
+"  PRIMARY KEY (`Device_DeviceID`, `Calendar_TaskID`),"
+"  INDEX `fk_Device_has_Calendar_Calendar1_idx` (`Calendar_TaskID` ASC),"
+"  INDEX `fk_Device_has_Calendar_Device1_idx` (`Device_DeviceID` ASC),"
+"  CONSTRAINT `fk_Device_has_Calendar_Calendar1`"
+"    FOREIGN KEY (`Calendar_TaskID`)"
+"    REFERENCES "+dName+".`Calendar` (`TaskID`)"
+"    ON DELETE NO ACTION"
+"    ON UPDATE NO ACTION,"
+"  CONSTRAINT `fk_Device_has_Calendar_Device1`"
+"  FOREIGN KEY (`Device_DeviceID`)"
+"  REFERENCES "+dName+".`Device` (`DeviceID`)"
+"   ON DELETE NO ACTION"
+"   ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Employee` ("
+"  `EmployeeID` INT(11) NOT NULL AUTO_INCREMENT,"
+"  `EmployeeName` VARCHAR(45) NOT NULL,"
+"  `JobTitle` VARCHAR(45) NOT NULL,"
+"  `EmployeeAddress` VARCHAR(45) NOT NULL,"
+"  `EmployeeDepartment` VARCHAR(15) NOT NULL,"
+"  `EmployeeEmail` VARCHAR(45) NOT NULL,"
+"  PRIMARY KEY (`EmployeeID`),"
+"  UNIQUE INDEX `EmployeeID_UNIQUE` (`EmployeeID` ASC),"
+"  UNIQUE INDEX `EmployeeName_UNIQUE` (`EmployeeName` ASC),"
+"  UNIQUE INDEX `EmployeeEmail_UNIQUE` (`EmployeeEmail` ASC))"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 13"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Phone` ("
+"  `PhoneNum` CHAR(20) NOT NULL,"
+"  `Employee_EmployeeID` INT(11) NOT NULL,"
+"  PRIMARY KEY (`PhoneNum`, `Employee_EmployeeID`),"
+"  INDEX `fk_Phone_Employee1_idx` (`Employee_EmployeeID` ASC),"
+"  CONSTRAINT `fk_Phone_Employee1`"
+"    FOREIGN KEY (`Employee_EmployeeID`)"
+"    REFERENCES "+dName+".`Employee` (`EmployeeID`)"
+"    ON DELETE NO ACTION"
+"    ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`User` ("
+"  `UserID` INT(11) NOT NULL AUTO_INCREMENT,"
+"  `UserName` VARCHAR(45) NOT NULL,"
+"  `Password` VARCHAR(45) NOT NULL,"
+"  `Employee_EmployeeID` INT(11) NOT NULL,"
+"  `Security` INT(1) NOT NULL,"
+"  PRIMARY KEY (`UserID`),"
+"  UNIQUE INDEX `UserID_UNIQUE` (`UserID` ASC),"
+"  UNIQUE INDEX `UserName_UNIQUE` (`UserName` ASC),"
+"  UNIQUE INDEX `Employee_EmployeeID_UNIQUE` (`Employee_EmployeeID` ASC),"
+"  INDEX `fk_User_Employee1_idx` (`Employee_EmployeeID` ASC),"
+"  CONSTRAINT `fk_User_Employee1`"
+"    FOREIGN KEY (`Employee_EmployeeID`)"
+"    REFERENCES "+dName+".`Employee` (`EmployeeID`)"
+"    ON DELETE NO ACTION"
+"    ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 1"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`User_has_Calendar` ("
+"  `User_UserID` INT(11) NULL DEFAULT '0',"
+"  `Calendar_TaskID` INT(11) NULL DEFAULT '0',"
+"  PRIMARY KEY (`User_UserID`, `Calendar_TaskID`),"
+"  INDEX `fk_User_has_Calendar_Calendar1_idx` (`Calendar_TaskID` ASC),"
+"  INDEX `fk_User_has_Calendar_User1_idx` (`User_UserID` ASC),"
+"  CONSTRAINT `fk_User_has_Calendar_Calendar1`"
+"    FOREIGN KEY (`Calendar_TaskID`)"
+"    REFERENCES "+dName+".`Calendar` (`TaskID`)"
+"    ON DELETE NO ACTION"
+"    ON UPDATE NO ACTION,"
+"  CONSTRAINT `fk_User_has_Calendar_User1`"
+"    FOREIGN KEY (`User_UserID`)"
+"    REFERENCES "+dName+".`User` (`UserID`)"
+"    ON DELETE NO ACTION"
+"   ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("INSERT INTO Employee (EmployeeID, EmployeeName, JobTitle, EmployeeAddress, EmployeeDepartment, EmployeeEmail)"
		+" VALUES ('0', 'admin', 'admin', 'admin', 'admin', 'admin@admin.com')")
con.commit()

cur.execute("INSERT INTO User (UserName, Password, Employee_EmployeeID, Security)"
		+" VALUES ('admin', 'admin',(SELECT EmployeeID FROM Employee WHERE EmployeeName = 'admin'),'2')")
con.commit()

con.close()

