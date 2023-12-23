jQuery(document).ready(function($) {
    $('#multiTable').DataTable({
        "ajax": {
            "url": multi_table_datatable_ajax_object.ajax_url + '?action=get_multi_table_data',
            "type": "POST",
            "data": {
                "nonce": multi_table_datatable_ajax_object.nonce
            }
        },
        "columns": [
            { "data": "column1" },
            { "data": "column2" },
            { "data": "column3" },
            // Add more columns as needed
        ]
    });
});

