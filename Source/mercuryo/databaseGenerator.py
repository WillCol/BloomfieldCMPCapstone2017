#!/bin/python
# python program
import MySQLdb as db
import sys

con = db.connect(user="root",passwd="root")
cur = con.cursor()

dName = raw_input("Input Database Name: ")
sys.stdout = open('dbconfig.txt', 'w')
print dName
sys.stdout.close()

cur.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
cur.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
cur.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';")

cur.execute('CREATE SCHEMA IF NOT EXISTS '+dName+' DEFAULT CHARACTER SET utf8;')
#cur.execute('CREATE SCHEMA IF NOT EXISTS `mrcInventory` DEFAULT CHARACTER SET utf8;')


con = db.connect(host="localhost",user="root",passwd="root",db=dName)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Task`"
	+" (`TaskType` INT(11) NOT NULL AUTO_INCREMENT,`TaskDesc` VARCHAR(45) NOT NULL, PRIMARY KEY (`TaskType`),"
  	+" UNIQUE INDEX `TaskDesc_UNIQUE` (`TaskDesc` ASC),"
  	+" UNIQUE INDEX `TaskType_UNIQUE` (`TaskType` ASC))"
	+" ENGINE = InnoDB"
	+" AUTO_INCREMENT = 889"
	+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Calendar` ("
  +" `TaskID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `DateStart` DATE NOT NULL,"
  +" `DateComplete` DATE NULL DEFAULT NULL,"
  +" `TaskStatus` VARCHAR(45) NOT NULL,"
  +" `Task_TaskType` INT(11) NOT NULL,"
  +" PRIMARY KEY (`TaskID`),"
  +" UNIQUE INDEX `TaskID_UNIQUE` (`TaskID` ASC),"
  +" INDEX `fk_Calendar_Task1_idx` (`Task_TaskType` ASC),"
  +" CONSTRAINT `fk_Calendar_Task1`"
   +"  FOREIGN KEY (`Task_TaskType`)"
   +" REFERENCES "+dName+".`Task` (`TaskType`)"
   +" ON DELETE NO ACTION"
   +" ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 11"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`DeviceStatus` ("
  +" `StatusID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `StatusDesc` VARCHAR(45) NOT NULL,"
  +" PRIMARY KEY (`StatusID`),"
  +" UNIQUE INDEX `StatusID_UNIQUE` (`StatusID` ASC))"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 33334"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Device` ("
  +" `DeviceID` INT(11) NOT NULL AUTO_INCREMENT,"
  +" `DeviceName` VARCHAR(25) NOT NULL,"
  +" `Description` VARCHAR(45) NULL DEFAULT NULL,"
  +" `DeviceCategory` VARCHAR(15) NOT NULL,"
  +" `DeviceStatus_StatusID` INT(11) NOT NULL,"
  +" `DeviceLocation` VARCHAR(45) NOT NULL,"
  +" `DeviceOwner` VARCHAR(45) NOT NULL,"
  +" `DateOfDeployment` DATE NOT NULL,"
  +" `GoBackDate` DATE NOT NULL,"
  +" `IPAddress` INT(11) NOT NULL,"
  +" `SerialNumber` INT(11) NOT NULL,"
  +" PRIMARY KEY (`DeviceID`),"
  +" UNIQUE INDEX `DeviceID_UNIQUE` (`DeviceID` ASC),"
  +" UNIQUE INDEX `SerialNumber_UNIQUE` (`SerialNumber` ASC),"
  +" INDEX `fk_Device_DeviceStatus1_idx` (`DeviceStatus_StatusID` ASC),"
  +" CONSTRAINT `fk_Device_DeviceStatus1`"
  +" FOREIGN KEY (`DeviceStatus_StatusID`)"
  +" REFERENCES "+dName+".`DeviceStatus` (`StatusID`)"
  +" ON DELETE NO ACTION"
  +" ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 100000"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Device_has_Calendar` ("
+"  `Device_DeviceID` INT(11) NOT NULL,"
+"  `Calendar_TaskID` INT(11) NOT NULL,"
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
+"  UNIQUE INDEX `EmployeeID_UNIQUE` (`EmployeeID` ASC))"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 13"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`Phone` ("
+"  `PhoneNum` CHAR(11) NOT NULL,"
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
+"  `Security` INT(11) NOT NULL,"
+"  PRIMARY KEY (`UserID`),"
+"  UNIQUE INDEX `UserID_UNIQUE` (`UserID` ASC),"
+"  UNIQUE INDEX `UserName_UNIQUE` (`UserName` ASC),"
+"  UNIQUE INDEX `Password_UNIQUE` (`Password` ASC),"
+"  UNIQUE INDEX `Employee_EmployeeID_UNIQUE` (`Employee_EmployeeID` ASC),"
+"  INDEX `fk_User_Employee1_idx` (`Employee_EmployeeID` ASC),"
+"  CONSTRAINT `fk_User_Employee1`"
+"    FOREIGN KEY (`Employee_EmployeeID`)"
+"    REFERENCES "+dName+".`Employee` (`EmployeeID`)"
+"    ON DELETE NO ACTION"
+"    ON UPDATE NO ACTION)"
+" ENGINE = InnoDB"
+" AUTO_INCREMENT = 901"
+" DEFAULT CHARACTER SET = utf8;")

cur.execute("CREATE TABLE IF NOT EXISTS "+dName+".`User_has_Calendar` ("
+"  `User_UserID` INT(11) NOT NULL,"
+"  `Calendar_TaskID` INT(11) NOT NULL,"
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

