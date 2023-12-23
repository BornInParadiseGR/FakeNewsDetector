<?php
/*
Plugin Name: Flask Data Display
Description: Plugin to display data fetched from Flask API using DataTables
Version: 1.0
Author: Your Name
*/
function enqueue_plugin_scripts() {
    wp_enqueue_style('datatables-css', 'https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css');
    wp_deregister_script('jquery');
    // Register and enqueue your preferred version of jQuery
    wp_register_script('jquery', 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', array(), '3.6.0', true);
    wp_enqueue_script('jquery');
    wp_enqueue_script('datatables-js', 'https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js', array('jquery'));
}
add_action('wp_enqueue_scripts', 'enqueue_plugin_scripts');

function display_flask_data_using_datatables() {
    ?>
	<head>
		<httpProtocol>
      		<customHeaders>
				<add name="Access-Control-Allow-Origin" value="*" />
				<add name="Access-Control-Allow-Headers" value="Content-Type" />
				<add name="Access-Control-Allow-Methods" value="GET, POST, PUT, DELETE, OPTIONS" />
      		</customHeaders>
    	</httpProtocol>
		<style>
			.fullscreen-modal {
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				z-index: 99;
				background-color: rgba(0, 0, 0, 0.8);
				color: white;
				padding: 4rem;
				overflow: scroll
			}
		</style>
	</head>
	<div id="article-modal" class="fullscreen-modal"></div>
    <table id="data" class="table table-striped">
        <thead>
            <tr>
                <!-- Define your table headers -->
                <th>ID</th>
                <th>Start Date</th>
                <th>End Date</th>
				<th>Status</th>
				<th>Actions</th>
            </tr>
        </thead>
		<tbody></tbody>
    </table>
	<table id="data-more" class="table table-striped">
        <thead>
            <tr>
                <!-- Define your table headers -->
                <th>ID</th>
                <th>Title</th>
                <th>Content</th>
				<th>Date</th>
				<th>Analysis Result</th>
            </tr>
        </thead>
		<tbody></tbody>
    </table>
	<button id="back-button">Back</button>

	<script>
		var table = null;
		var table_more = null;
		var user_id = <?php echo get_current_user_id(); ?>;
		
		function initTable() {
			table = new DataTable('#data', {
				ajax: 'http://localhost:5000/getDbData?user_id='+user_id,
				columns: [
					{ data: 'analysisId' },
					{ data: 'startTime' },
					{ data: 'endTime' },
					{ data: 'status' },
					{
						defaultContent: '<button class="go-to-analysis-btn">View more</button> <button class="delete-analysis-btn btn btn-danger">Delete</button>'
					}
				]
			});
			table.on('click', '.go-to-analysis-btn', function (e) {
				let data = table.row(e.target.closest('tr')).data();
			
				let url = 'http://localhost:5000/getDbData?user_id='+user_id+'&analyze_id='+data["analysisId"];
				table_more = new DataTable('#data-more', {
					ajax: url,
					columns: [
						{ data: 'articleId' },
						{ data: 'title' },
						{
							data: 'content' ,
							className : "expandable-article-content"
						},
						{ data: 'date' },
						{ data: 'isFake' }
					]
				});
				table_more.on('click', '.expandable-article-content', function(e) {
					let tdata = table_more.row(e.target.closest('tr')).data();
					let article_id = tdata["articleId"];
					$.getJSON( "http://localhost:5000/getArticleFullContent?article_id="+article_id, function(data) {
						$('#article-modal').text(data.data);
						$('#article-modal').show();
					});
				});
				$('#data').hide()
				$('#data-more').show()
				table.clear()
				table.destroy()
			});
			table.on('click', '.delete-analysis-btn', function (e) {
				table.ajax.reload()
				let data = table.row(e.target.closest('tr')).data();
				
				if (confirm("Are you sure you want to delete all analysis data? This action cannot be undone!")) {
					let url = 'http://localhost:5000/deleteAnalysis?analysis_id='+data["analysisId"];
					$.get(url, function(datata) {
						table.ajax.reload()
					})
				}
			});
		}

		$(document).ready(function () {
			$('#article-modal').hide();
			$('#data-more').hide();
			initTable();
			$('#back-button').on('click', function(e) {
				$('#data-more').hide();
				table_more.clear()
				table_more.destroy()
				initTable()
				$('#data').show()
			});
			
			$('#show-modal').on('click', function(e) {
  				$('#article-modal').show();
  			});

			$('#article-modal').on('click', function(e) {
			  	$('#article-modal').hide();
			});
		});
	</script>
    <?php
}
add_shortcode('display_flask_data', 'display_flask_data_using_datatables');