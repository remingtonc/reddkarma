$(document).ready(function() {
	setupSearch();
	init();
});

function setupSearch() {
	$("#searchSubmit").on('click', function() {
		window.location = "http://192.241.216.69"+$("#search").val();
	});
}