
$(function() {
 
 $("form[name='addDevice']").validate({
    
			rules: {
			  computer: "required",
			  Desc: "required",
			 deviceCategory:"required",
			 location: "required",
			 deviceStatus:"required",
			 owner:"required",
			 dateOfDeployment:"required",
			 backDate:"required",
			 IP:"required",
			 serialNumber:"required",		  
			},
		   
			messages: {
			computer: "Please enter a Device Name",
			  Desc: "Please enter a Description",
			 deviceCategory:"Please enter a Device Category",
			 location: "Please enter a Device Location",
			 owner:"Please enter a  Device Owner",
			 dateOfDeployment:"Please enter a Date of Deployment",
			 backDate:"Please enter a Go-Back Date",
			 IP:"Please enter an IP Address",
			 serialNumber:"Please enter a Serial Number",
			 deviceStatus:"Please enter a valid Device Status"
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
  
  $("form[name='adddevicestatus']").validate
	  ({
		
				rules: {
				  StatusID: "required",
				  StatusDesc: "required", 
				},
			   
				messages: {
				 StatusID: "Please enter  a Status ID.",
				  StatusDesc: "Please enter a Status Desc.",
				},
				
				submitHandler: function(form) {
				  form.submit();
				}
		});
	

	$("form[name='addUser']").validate({
    
			rules: {
			  UserID: "required",
			  UserName: "required",
			  Security: "required",
			  EmployeeID: "required",
				Password: {
				required: true,
				minlength: 5
			  }
			  
			},
			// Specify validation error messages
			messages: {
			 UserID: "Please enter a UserID",
			  UserName: "Please enter a UserName",
			  Security: "Please enter a Security Field",
			  EmployeeID: "Please enter a EmployeeID",
			  Password: {
				required: "Please enter a password",
				minlength: "Your password must be at least 5 characters long"
			  },
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
	
	$("form[name='addTask']").validate({
    
			rules: {
			  DateStart: "required",
			  DateComplete: "required",
			  TaskStatus: "required",
			  Task_TaskType:"required",
			},
			// Specify validation error messages
			messages: {
			 DateStart: "Please enter a Start Date",
			  DateComplete: "Please enter a Completion Date",
			  TaskStatus: "Please enter a TaskStatus",
			  Task_TaskType:"Please enter a Task Type",
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
 
	$("form[name='addtasktype']").validate({
    
			rules: {
			  TaskTypeID: "required",
			  TaskDesc: "required",
			},
			// Specify validation error messages
			messages: {
			 TaskTypeID: "Please enter a Task Type ID",
			  TaskDesc: "Please enter a Task Desc",
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
 	
 
 $("form[name='addEmployee']").validate({

			rules: {
			  EmployeeName: "required",
			  JobTitle: "required",
			  EmployeeAddress: "required",
			  EmployeeDepartment: "required",
			  EmployeePhoneNumber:{phoneUs: true,
			  required: true
			  },
			  EmployeeEmail: {
				required: true,
				email: true
			  },
			  
			},
		   
			messages: {
			  EmployeeName: "Please enter a Employee Name",
			  JobTitle: "Please enter a Job Title",
			  EmployeeAddress: "Please enter a Employee Address",
			  EmployeeDepartment: "Please enter a Employee Department",
			  EmployeeEmail: "Please enter a valid Employee Email",
			  EmployeePhoneNumber: "Please enter a valid Phone Number"
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
 $("form[name='editDevice']").validate({
    
			rules: {
			  computer: "required",
			  Desc: "required",
			 deviceCategory:"required",
			 location: "required",
			 owner:"required",
			 dateOfDeployment:"required",
			 backDate:"required",
			 IP:"required",
			 serialNumber:"required",		  
			},
		   
			messages: {
			computer: "Please enter a Device Name",
			  Desc: "Please enter a Desc",
			 deviceCategory:"Please enter a Device Category",
			 location: "Please enter a Device Location",
			 owner:"Please enter a  Device Owner",
			 dateOfDeployment:"Please enter a Date of Deployment",
			 backDate:"Please enter a Go-Back Date",
			 IP:"Please enter an IP Address",
			 serialNumber:"Please enter a Serial Number",
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
  
  $("form[name='editDeviceStatus']").validate
	  ({
		
				rules: {
				  StatusID: "required",
				  StatusDesc: "required", 
				},
			   
				messages: {
				 StatusID: "Please enter  a Status ID.",
				  StatusDesc: "Please enter a Status Desc.",
				},
				
				submitHandler: function(form) {
				  form.submit();
				}
		});
	

	$("form[name='editUser']").validate({
    
			rules: {
			  UserID: "required",
			  UserName: "required",
			  Security: "required",
			  EmployeeID: "required",
				Password: {
				required: true,
				minlength: 5
			  }
			  
			},
			// Specify validation error messages
			messages: {
			 UserID: "Please enter a UserID",
			  UserName: "Please enter a UserName",
			  Security: "Please enter a Security Field",
			  EmployeeID: "Please enter a EmployeeID",
			  Password: {
				required: "Please enter a password",
				minlength: "Your password must be at least 5 characters long"
			  },
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
	
	$("form[name='editTask']").validate({
    
			rules: {
			  DateStart: "required",
			  DateComplete: "required",
			  TaskStatus: "required",
			  Task_TaskType:"required",
			},
			// Specify validation error messages
			messages: {
			 DateStart: "Please enter a Start Date",
			  DateComplete: "Please enter a Completion Date",
			  TaskStatus: "Please enter a TaskStatus",
			  Task_TaskType:"Please enter a Task Type",
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
 
	$("form[name='editTaskType']").validate({
    
			rules: {
			  TaskType: "required",
			  TypeDesc: "required",
			},
			// Specify validation error messages
			messages: {
			 TaskType: "Please enter a Task Type",
			  TypeDesc: "Please enter a Task Desc",
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
 	
 
 $("form[name='editEmployee']").validate({

			rules: {
			  EmployeeName: "required",
			  JobTitle: "required",
			  EmployeeAddress: "required",
			  EmployeeDepartment: "required",
			  EmployeeEmail: {
				required: true,
				email: true
			  },
			  
			},
		   
			messages: {
			  EmployeeName: "Please enter a Employee Name",
			  JobTitle: "Please enter a Job Title",
			  EmployeeAddress: "Please enter a Employee Address",
			  EmployeeDepartment: "Please enter a Employee Department",
			  EmployeeEmail: "Please enter a valid Employee Email"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	$("form[name='deleteemployee']").validate({

			rules: {
			  EmployeeID: "required",
			  
			  
			},
		   
			messages: {
			  EmployeeName: "Please enter a Employee Name",
			  JobTitle: "Please enter a Job Title",
			  EmployeeAddress: "Please enter a Employee Address",
			  EmployeeDepartment: "Please enter a Employee Department",
			  EmployeeEmail: "Please enter a valid Employee Email"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	 
	 $("form[name='deleteDevice']").validate({
    
			rules: {
			 deviceID:"required",		  
			},
		   
			messages: {
			deviceID:"Please enter a valid device ID"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
   $("form[name='deleteTask']").validate({
    
			rules: {
			 taskID:"required",		  
			},
		   
			messages: {
			taskID:"Please enter a valid Task ID"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	  $("form[name='deleteTaskType']").validate({
    
			rules: {
			 taskType:"required",		  
			},
		   
			messages: {
			taskType:"Please enter a valid Task Type"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	  $("form[name='deleteDeviceStatus']").validate({
    
			rules: {
			 statusID:"required",		  
			},
		   
			messages: {
			statusID:"Please enter a valid status ID"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	 $("form[name='deleteEmployee']").validate({
    
			rules: {
			 EmployeeID:"required",		  
			},
		   
			messages: {
			EmployeeID:"Please enter a valid Employee ID"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
	  $("form[name='deleteuser']").validate({
    
			rules: {
			 UserID:"required",		  
			},
		   
			messages: {
			UserID:"Please enter a valid User ID"
			   
			  
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	 });
 });