$(document).ready(init);

function init() {
	setupSearch();
    getKarma();
    getDomains();
    initializeHourlyChart();
}

function setupSearch() {
	$("#searchSubmit").on('click', function() {
		window.location = "http://192.241.216.69"+$("#search").val();
	});
}

/**
 * Get the total and average karma per post for the subreddit.
 */
function getKarma() {
    $.get("/karma/"+subreddit).done(function(data) {
            data = JSON.parse(data);
            console.log("totalkarma: " + data[0].f[0].v);
            $("#totalKarma").html(data[0].f[0].v);
            console.log("averagekarma: " + data[0].f[1].v);
            $("#avgKarma").html(data[0].f[1].v);
    });
}

/**
 * Get the top domains used by submissions for the subreddit.
 * Fetches the domain, total karma, and average karma per post.
 */
function getDomains() {
	$.get("/domains/"+subreddit).done(function(data) {
		data = JSON.parse(data);
		outputStr = "";
		for (var i in data)
			outputStr += "<tr><td>"+data[i].f[0].v+"</td><td>"+data[i].f[1].v+"</td><td>"+data[i].f[2].v+"</td></tr>";
		$("#submissionDomains").append(outputStr);
	});
}

/**
 * Initialize the hourly chart layout and content.
 * Bar chart, AM/PM breakdown.
 * Fetches the average karma per hour for the subreddit.
 */
function initializeHourlyChart() {
    var chartData = {
            labels: [],
            datasets: [
                {
                    label: "Karma By Hour",
                    fillColor: "rgba(151,187,205,0.5)",
		            strokeColor: "rgba(151,187,205,0.8)",
		            highlightFill: "rgba(151,187,205,0.75)",
		            highlightStroke: "rgba(151,187,205,1)",
                    data: []
                }
            ]
    };
    for (var i = 0; i < 24; i++)
            chartData.labels[i] = ((i==0 || i==12) ? 12 : (i % 12)) + " " + ((i < 12) ? "AM" : "PM");
    var ctx = document.getElementById("hourlyChart").getContext("2d");
    $.get("/hourly/"+subreddit).done(function(data) {
            data = JSON.parse(data);
            for (var i in data) {
                    console.log(data[i].f[1].v);
                    chartData.datasets[0].data.push(data[i].f[1].v);
            }
            var hourlyChart = new Chart(ctx).Bar(chartData, {});
    });
}
