<?php
defined( 'ABSPATH' ) OR exit;

function wpa_remove_title_meta_box() {

	$screens = array( 'post', 'page' );

	foreach ( $screens as $screen ) {

		$title = esc_html__( 'Remove Page Title', 'remove-page-title' );
		if ( $screen == 'post' ) {
			$title = esc_html__( 'Remove Post Title', 'remove-page-title' );
		}

		add_meta_box(
			'wpa_remove_title',
			$title,
			'wpa_remove_title_callback',
			$screen,
			'side'
		);
	}
}
add_action( 'add_meta_boxes', 'wpa_remove_title_meta_box' );

function wpa_remove_title_callback( $post ) {

	wp_nonce_field( 'wpa_remove_title', 'wpa_remove_title_nonce' );

	$remove_title = get_post_meta( $post->ID, 'wpa_remove_title', true );

	echo '<label for="wpa_remove_title">';
		echo '<input type="checkbox" name="wpa_remove_title" id="wpa_remove_title" value="1" ' . checked( '1', $remove_title, false ) . '>';
		esc_html_e( 'Remove the title', 'remove-page-title' );
	echo '</label> ';
}

function wpa_remove_title_save_data( $post_id ) {

	global $post;

	if ( ! isset( $_POST['wpa_remove_title_nonce'] ) ) {
		return;
	}
	if ( ! wp_verify_nonce( $_POST['wpa_remove_title_nonce'], 'wpa_remove_title' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	/* it's safe to save the data now. */

	if ( ! isset( $_POST[ 'wpa_remove_title' ] ) ) {
		$_POST[ 'wpa_remove_title' ] = '0';
	}
	$setting = $_POST[ 'wpa_remove_title' ];

	if ( $setting == '1' || $setting == '0' ) {
		update_post_meta( $post_id, 'wpa_remove_title', $setting );
	}
}
add_action( 'pre_post_update', 'wpa_remove_title_save_data' );