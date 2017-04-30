$(document).ready(function() {
    
<!-- Initalize DataTable --!>	 
	var dataTable= $('#Table').DataTable( {

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
        },{
			"targets": [ 1 ],
			 "visible": false
		} ],
        order: [ 1, 'asc' ]
    } );

			 $("#submitButton").hide();
			  
			 $('.showHideColumn').on( 'click', function (e) {
				e.preventDefault();
 
        // Get the column API object
        var column = dataTable.column( $(this).attr('data-column') );
 
        // Toggle the visibility
        column.visible( ! column.visible() );
		$("#submitButton").toggle();



   } );

} );