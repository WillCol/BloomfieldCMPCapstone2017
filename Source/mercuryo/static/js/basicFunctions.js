$(document).ready(function() {
     
<!-- Initalize DataTable --!>	 
	 $('#Table').DataTable( {
         buttons: [
        'copy', 'excel', 'pdf'
    ],
		responsive: {
            details: {
                type: 'column'
            }
        },
        columnDefs: [ {
            className: 'control',
            orderable: false,
            targets:   0
        } ],
        order: [ 1, 'asc' ]
    } );
			  
			  
	<!-- "Allows deleteButton to toggle the delete column within tables" --!>	   
	 $("#submitButton").hide();
     $('td:nth-child(2),th:nth-child(2)').hide();
	 $('#deleteButton').click(function() 
		{
		$('td:nth-child(2),th:nth-child(2)').toggle();
		$("#submitButton").toggle();
                
    });
} );