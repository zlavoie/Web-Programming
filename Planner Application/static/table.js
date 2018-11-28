$(document).ready(function() {
    // create a data table from existing html table
    table = $('#table').DataTable();

    // set event handler for row click
    $('#table tbody').on('click', 'tr', function () {
	var rowthis = this; 	                            // save this for callback use later
        var row = table.row( this ).data();                 // get row using datatable api

    } );
} );
