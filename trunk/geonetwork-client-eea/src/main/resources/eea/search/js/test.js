$(document).ready(function() {
	var height = $('#firstHeader').outerHeight();
	if (height !== null) {
		$('#slide-button').height(height)
	}
	$('#slide-button').click(function() {
		var body = $('body');
		var menu = $('#slide-menu');
		var button = $(this);
		var content = $('#content');
		var leftColumn = $('#portal-column-one');
		var maximizeMenu = function() {
			leftColumn.animate({
				'left' : '0'
			})
		};
		var minimizeMenu = function() {
			leftColumn.animate({
				'left' : '-' + menu.width()
			})
		};
		var maximizeContent = function() {
			content.animate({
				'marginLeft' : button.width()
			})
		};
		var minimizeContent = function() {
			content.animate({
				'marginLeft' : leftColumn.width()
			})
		};
		var goFullScreen = function() {
			body.addClass('fullscreen');
			maximizeContent();
			minimizeMenu()
		};
		var exitFullScreen = function() {
			body.removeClass('fullscreen');
			minimizeContent();
			maximizeMenu()
		};
		if (body.hasClass('fullscreen')) {
			exitFullScreen()
		} else {
			goFullScreen()
		}
	});
	if ($('body').hasClass('fullscreen')) {
		$('#slide-button').click()
	}
});
