
$(function() {
  
  $("form[name='addDeviceStatus']").validate
	  ({
		
				rules: {
				  StatusID: "required",
				  StatusDesc: "required", 
				},
			   
				messages: {
				 StatusID: "Please enter  a Status ID.",
				  StatusDesc: "Please enter a Status Description.",
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
	
	
	$("form[name='addTaskType']").validate({
    
			rules: {
			  TaskType: "required",
			  TypeDesc: "required",
			},
			// Specify validation error messages
			messages: {
			 TaskType: "Please enter a Task Type",
			  TypeDesc: "Please enter a Task Description",
			},
			// Make sure the form is submitted to the destination defined
			// in the "action" attribute of the form when valid
			submitHandler: function(form) {
			  form.submit();
			}
	});
 
 
 $("form[name='addEmployee']").validate({
    
			rules: {
			  EmployeeID: "required",
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
			  EmployeeID: "Please enter a Employee ID",
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

	 
	
 });