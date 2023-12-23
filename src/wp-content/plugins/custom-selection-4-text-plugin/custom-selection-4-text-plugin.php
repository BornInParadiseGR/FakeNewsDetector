<?php
/*
Plugin Name: Docker Flask Form
Description: A WordPress plugin with a selection input that shows only the selected option.
Version: 2.0
Author: Panagiotis Antoniou
*/

// Enqueue your JavaScript and CSS files
function enqueue_custom_scripts() {
    wp_enqueue_script('custom-scripts', plugin_dir_url(__FILE__) . 'custom-scripts.js', array('jquery'), '1.0', true);
}
add_action('wp_enqueue_scripts', 'enqueue_custom_scripts');

// Create the HTML content for the selection input and four text inputs
    function custom_selection_text_input() {
    ob_start();
    ?>
	<head>
	<httpProtocol>
      <customHeaders>
        <add name="Access-Control-Allow-Origin" value="*" />
        <add name="Access-Control-Allow-Headers" value="Content-Type" />
        <add name="Access-Control-Allow-Methods" value="GET, POST, PUT, DELETE, OPTIONS" />
      </customHeaders>
    </httpProtocol>
	</head>
	<label for="custom-select">Choose an option:</label>
	<select id="custom-select">
		<option value="data1">Text Data</option>
		<option value="data2">Url</option>
		<option value="data3">Datas File</option>
		<option value="data4">Urls File</option>
	</select>
	<form method="POST" id="json-form">
		<div id="text-input-1">
			<br>
			 <!-- <input type="text" id="name" name="name" >  -->
			<label for="title_text_field">Title:</label>
			<input type="text" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" id="title_text_field" name="title_text_field">
			<label for="date_text_field">Date:</label>
			<input type="text" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" id="date_text_field" style="width:150px" name="date_text_field">
			<label for="text_field">Content:</label>
			<textarea cols="40" rows="10" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" aria-invalid="false" name="text_field" id="text_field"></textarea>
		</div>

		<div id="text-input-2">
			<br>
			<label for="url_field">Write Url:</label>
            <input type="text" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" id="url_field" name="url_field">
		</div>
		
		<div id="text-input-3">
			<br>
			<label for="text_file_field" >Upload File with Urls:</label>
			 <!-- <input type="text" id="name" name="name" >  -->
			<input type="file" name="csvFile" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" accept=".csv" name="text_file_field" id="text_file_field">
		</div>

		<div id="text-input-4">
			<br>
			<label for="url_file_field">Upload File with Datas:</label>
			 <!-- <input type="text" id="name" name="name" >  -->
			<input type="file" name="csvFile" class="wpcf7-form-control wpcf7-textarea wpcf7-validates-as-required" aria-required="true" accept=".csv" name="url_file_field" id="url_file_field">
		</div>
		<br>
		<div id="messageContainer"></div>
        <input type="button" id="submitBtn" name="submit" value="Submit">
	</form>
	<div id="form-response"></div>

	<script>
        jQuery(document).ready(function ($) {
            $('#submitBtn').on("click", function (event) {
				event.preventDefault();
				$('#form-response').html("");
				var user_id = <?php echo get_current_user_id(); ?>;
				var data_type = $('#custom-select').val();
				if (data_type == 'data1') {
					var formData = {
						data: $('#text_field').val(),
						title: $('#title_text_field').val(),
						date: $('#date_text_field').val(),
						user_id: user_id,
					};
					$.ajax({
						type: 'POST',
						url: 'http://localhost:5000/dataForm',
						data: JSON.stringify(formData),
						contentType: 'application/json',
						success: function (result) {
							$('#form-response').html('Analysis result using'+result);
						},
						error: function (xhr, textStatus, errorThrown) {
							$('#form-response').html('Error: ' + textStatus);
						}	
					});	
				} else if (data_type == 'data2') {
					var formData = {
						data: $('#url_field').val(),
						user_id: user_id,
					};
					$.ajax({
						type: 'POST',
						url: 'http://localhost:5000/urlForm',
						data: JSON.stringify(formData),
						contentType: 'application/json',
						success: function (result) {
							$('#form-response').html('Analysis result using'+result);
						},
						error: function (xhr, textStatus, errorThrown) {
							$('#form-response').html('Error: ' + textStatus);
						}
					});	
				} else if (data_type == 'data3') {
					var inputField = $('#text_file_field')[0];
					if (inputField.files.length > 0) {
						var textfile = inputField.files[0];
						// Now you can work with the selected file
					}
					if(textfile){
						//const formData = new FormData();
						//formData.append('text-file', textfile, textfile.name);
						//formData.append('text_file_field', textfile);
						
						var reader = new FileReader();
						
						reader.onload = function(e)
						{
							var jsondata = new Object()
							jsondata.filename = textfile.name
							jsondata.contents = btoa(e.target.result);
							jsondata.user_id = user_id;
							$.ajax({
								type: 'POST',
								url: 'http://localhost:5000/textFileForm',
								data: JSON.stringify(jsondata),
								crossDomain: true,
								contentType: 'application/json',
								headers: {
									'Access-Control-Allow-Origin': '*',
									'Access-Control-Allow-Headers': 'x-requested-with'
								},
								success: function(result) {
									$('#form-response').html(result);
								}
							});
						};
						reader.readAsBinaryString(textfile);			
					}
				}
				else if (data_type == 'data4') {
					var inputField = $('#url_file_field')[0];
					if (inputField.files.length > 0) {
						var textfile = inputField.files[0];
						// Now you can work with the selected file
					}
					if(textfile){
						//const formData = new FormData();
						//formData.append('text-file', textfile, textfile.name);
						//formData.append('text_file_field', textfile);
						
						var reader = new FileReader();
						
						reader.onload = function(e)
						{
							var jsondata = new Object()
							jsondata.filename = textfile.name
							jsondata.contents = btoa(e.target.result);
							jsondata.user_id = user_id;
							
							$.ajax({
								type: 'POST',
								url: 'http://localhost:5000/urlFileForm',
								data: JSON.stringify(jsondata),
								crossDomain: true,
								contentType: 'application/json',
								headers: {
									'Access-Control-Allow-Origin': '*',
									'Access-Control-Allow-Headers': 'x-requested-with'
								},
								success: function(result) {
									$('#form-response').html(result);
								}
							});
						};
						reader.readAsBinaryString(textfile);			
					}
				}
            });
        });
    </script>

    <script>
        jQuery(document).ready(function($) {
            $('#custom-select').change(function() {
                const selectedOption = $(this).val();
				var data_type = $('#custom-select').val();
				var message = "Log in to use this option!";
				var user_id = <?php echo get_current_user_id(); ?>;
                // Hide all text input containers
                $('#messageContainer').html("");
                $('#text-input-1, #text-input-2, #text-input-3, #text-input-4').hide();
                // Show the selected text input container
                $(`#text-input-${selectedOption.charAt(selectedOption.length - 1)}`).show();

				if (user_id == 0 && data_type != 'data1' && data_type != 'data2'){
					$('#text-input-3, #text-input-4').hide();
					$('#messageContainer').text(message);
					
				}
            });

            // Trigger the change event to set the initial state
            $('#custom-select').trigger('change');
        });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode('custom_selection_text', 'custom_selection_text_input');