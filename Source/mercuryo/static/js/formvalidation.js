$(function() {
   
   
   <!-- Add Device  -->
    $("form[name='addDevice']").validate({

        rules: {
            computer: "required",
            Desc: "required",
            deviceCategory: "required",
            location: "required",
            deviceStatus: "required",
            owner: "required",
            dateOfDeployment: {
                date: true,
                required: true
            },
            backDate: {
                date: true,
                required: true
            },
            IP: "required",
            serialNumber: "required",
        },
        messages: {
            computer: "Please enter a Device Name",
            Desc: "Please enter a Description",
            deviceCategory: "Please enter a Device Category",
            location: "Please enter a Device Location",
            owner: "Please enter a  Device Owner",
            dateOfDeployment: {
                required: "Please enter a valid Date of Deployment",
                date: "Not a valid Date"
            },
            backDate: {
                required: "Please enter a valid Date of Deployment",
                date: "Not a valid Date"
            },
            IP: "Please enter an IP Address",
            serialNumber: "Please enter a Serial Number",
            deviceStatus: "Please enter a valid Device Status"

        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
    
	
	<!-- Add Device Status  -->
    $("form[name='adddevicestatus']").validate({

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

    
	<!-- Add User  -->
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
    
	
	<!-- Add Task  -->
    $("form[name='addTask']").validate({




        rules: {
            TaskName: "required",
            TaskLocation: "required",
            DateStarted: {
                date: true,
                required: true
            },
            DateCompleted: {
                date: true,
                required: true
            },
            TaskStatus: "required",
            Task_TaskType: "required",
        },
        // Specify validation error messages
        messages: {
            TaskName: "Please enter a Task Name",
            TaskLocation: "Please enter a Task Location",
            DateStarted: {
                required: "Please enter a Start Date",
                date: "Not a valid Date"
            },
            DateCompleted: "Please enter a Completion Date",
            TaskStatus: "Please enter a TaskStatus",
            Task_TaskType: "Please enter a Task Type",
            activeTask: "Must pick one of these fields"
        },

        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        },
        errorPlacement: function(error, element) {
            if (element.is(":radio")) {
                error.appendTo('#radio');
            } else {
                error.insertAfter(element);
            }
        },
    });
    
	
	<!-- Add Task Type  -->
    $("form[name='addtasktype']").validate({

        rules: {
            TaskName: "required",
            TaskDesc: "required",
        },
        // Specify validation error messages
        messages: {
            TaskName: "Please enter a Task Name",
            TaskDesc: "Please enter a Task Desc",
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }


    });

    
	<!-- Add Employee  -->
    $("form[name='addEmployee']").validate({

        rules: {
            EmployeeName: {
                lettersonly: true,
                required: true
            },
            JobTitle: "required",
            EmployeeAddress: "required",
            EmployeeDepartment: "required",
            EmployeePhoneNumber: {
                required: true,
                phoneUS: true
            },
            EmployeeEmail: {
                required: true,
                email: true
            },

        },

        messages: {
            EmployeeName: {
                required: "Please enter a Employee Name",
                lettersonly: "Must contain letters only"
            },
            JobTitle: "Please enter a Job Title",
            EmployeeAddress: "Please enter a Employee Address",
            EmployeeDepartment: "Please enter a Employee Department",
            EmployeeEmail: "Please enter a valid Employee Email",
            EmployeePhoneNumber: {
                required: "Please enter a valid Phone Number",
                phoneUS: "Not a valid Phone Number"
            },
        },

        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
   
   
    <!-- Add Device Category  -->
    $("form[name='adddevicecategory']").validate({

        rules: {
            CategoryName: "required",
            CategoryDesc: "required",
        },

        messages: {
            CategoryName: "Please enter a Category Name",
            CategoryDesc: "Please enter a Category Description",


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
   
   
    <!-- Edit Device  -->
    $("form[name='editDevice']").validate({


        rules: {
            computer: "required",
            Desc: "required",
            deviceCategory: "required",
            location: "required",
            deviceStatus: "required",
            owner: "required",
            dateOfDeployment: {
                date: true,
                required: true
            },
            backDate: {
                date: true,
                required: true
            },
            IP: "required",
            serialNumber: "required",
        },
        messages: {
            computer: "Please enter a Device Name",
            Desc: "Please enter a Description",
            deviceCategory: "Please enter a Device Category",
            location: "Please enter a Device Location",
            owner: "Please enter a  Device Owner",
            dateOfDeployment: {
                required: "Please enter a valid Date of Deployment",
                date: "Not a valid Date"
            },
            backDate: {
                required: "Please enter a valid Date of Deployment",
                date: "Not a valid Date"
            },
            IP: "Please enter an IP Address",
            serialNumber: "Please enter a Serial Number",
            deviceStatus: "Please enter a valid Device Status"

        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });

    <!-- Edit Device Status  -->
    $("form[name='editDeviceStatus']").validate({

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

    
	<!-- Edit User  -->
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
   
   
    <!-- Edit Task  -->
    $("form[name='editTask']").validate({
        errorElement: 'div',

        rules: {
            TaskName: "required",
            TaskLocation: "required",
            DateStarted: "required",
            DateCompleted: "required",

            TaskStatus: "required",
            Task_TaskType: "required",
        },
        // Specify validation error messages
        messages: {
            TaskName: "Please enter a Task Name",
            TaskLocation: "Please enter a Task Location",
            DateStarted: "Please enter a Start Date",
            DateCompleted: "Please enter a Completion Date",
            TaskStatus: "Please enter a TaskStatus",
            Task_TaskType: "Please enter a Task Type",
            activeTask: "One of these fields are required"
        },

        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        },
        errorPlacement: function(error, element) {
            if (element.is(":radio")) {
                error.appendTo('#radio');
            } else {
                error.insertAfter(element);
            }
        },
    });
    
	
	<!-- Edit Task Type  -->
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

    
	<!-- Edit Employee  -->
    $("form[name='editEmployee']").validate({

        rules: {
            EmployeeName: {
                lettersonly: true,
                required: true
            },
            JobTitle: "required",
            EmployeeAddress: "required",
            EmployeeDepartment: "required",
            EmployeeEmail: {
                required: true,
                email: true
            },

        },

        messages: {
            EmployeeName: {
                required: "Please enter a Employee Name",
                lettersonly: "Must contain letters only"
            },
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
    
	
	
	<!-- Edit Device Category  -->
    $("form[name='editdevicecategory']").validate({

        rules: {
            CategoryName: "required",
            CategoryDesc: "required",
        },

        messages: {
            CategoryName: "Please enter a Category Name",
            CategoryDesc: "Please enter a Category Description",


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
    
	
	
	<!-- Delete Employee -->
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
    
	
	
	<!-- Delete Device -->
    $("form[name='deleteDevice']").validate({

        rules: {
            deviceID: "required",
        },

        messages: {
            deviceID: "Please enter a valid device ID"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
    
	
	<!-- Delete Task -->
    $("form[name='deleteTask']").validate({

        rules: {
            taskID: "required",
        },

        messages: {
            taskID: "Please enter a valid Task ID"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });

    
	<!-- Delete Task Type -->
    $("form[name='deleteTaskType']").validate({

        rules: {
            taskType: "required",
        },

        messages: {
            taskType: "Please enter a valid Task Type"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });

    
	<!-- Delete Device Status -->
    $("form[name='deleteDeviceStatus']").validate({

        rules: {
            statusID: "required",
        },

        messages: {
            statusID: "Please enter a valid status ID"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
    
	
	<!-- Delete Employee -->
    $("form[name='deleteEmployee']").validate({

        rules: {
            EmployeeID: "required",
        },

        messages: {
            EmployeeID: "Please enter a valid Employee ID"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });
    
	
	
	<!-- Delete User -->
    $("form[name='deleteuser']").validate({

        rules: {
            UserID: "required",
        },

        messages: {
            UserID: "Please enter a valid User ID"


        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        }
    });



    jQuery.validator.addMethod("lettersonly", function(value, element) {
        return this.optional(element) || /^[a-z -]+$/i.test(value);
    }, "Letters only please");

    jQuery.validator.addMethod("phoneUS", function(phone_number, element) {
        phone_number = phone_number.replace(/\s+/g, "");
        return this.optional(element) || phone_number.length > 9 &&
            phone_number.match(/^(\+?1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
    });

    jQuery.validator.addMethod("date", function(date, element) {
        return this.optional(element) || date.match(/^\d{4}-((0\d)|(1[012]))-(([012]\d)|3[01])$/);
    }, "Please enter a valid date");
});