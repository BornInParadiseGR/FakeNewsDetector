<?php
/*
Plugin Name: Remove Page Title
Version: 1.0
Plugin URI: https://www.competethemes.com/blog/wordpress-remove-page-title/
Description: Remove the title from any post or page in seconds. You can find the option to hide titles in the right sidebar of the post editor. Remove Page Title is compatible with the Gutenberg editor and the classic editor.
Author: Compete Themes
Author URI: https://www.competethemes.com/
Text Domain: remove-page-title
Domain Path: /languages
License: GNU General Public License v2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html
*/

// set constant for main plugin files
if ( ! defined( 'WPA_REMOVE_PAGE_TITLE_FILE' ) ) {
  define( 'WPA_REMOVE_PAGE_TITLE_FILE', __FILE__ );
}

// set constant for plugin directory
if ( ! defined( 'WPA_REMOVE_PAGE_TITLE_PATH' ) ) {
  define( 'WPA_REMOVE_PAGE_TITLE_PATH', plugin_dir_path( WPA_REMOVE_PAGE_TITLE_FILE ) );
}

// set constant for plugin url
if ( ! defined( 'WPA_REMOVE_PAGE_TITLE_URL' ) ) {
  define( 'WPA_REMOVE_PAGE_TITLE_URL', plugin_dir_url( __FILE__ ) );
}

// set constant for plugin basename
if ( ! defined( 'WPA_REMOVE_PAGE_TITLE_BASENAME' ) ) {
  define( 'WPA_REMOVE_PAGE_TITLE_BASENAME', plugin_basename( WPA_REMOVE_PAGE_TITLE_FILE ) );
}

require_once( WPA_REMOVE_PAGE_TITLE_PATH . 'meta-box.php' );

function wpa_remove_page_titles( $title ) {

  global $post;

  if ( !is_admin() && in_the_loop() && is_singular() ) {
    if ( get_post_meta( $post->ID, 'wpa_remove_title', true ) ) {
      return '<span style="position: absolute; rect(1px, 1px, 1px, 1px); overflow: hidden; height: 1px; width: 1px;">'. $title .'</span>';
    } else {
      return $title;
    }
  } else {
    return $title;
  }
}
add_filter( 'the_title', 'wpa_remove_page_titles', 99 );