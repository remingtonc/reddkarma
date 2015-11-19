$(document).ready(init);

function init() {
        getKarma();
        initializeHourlyChart();
}

/**
 * Get the total and average karma for the subreddit
 * and apply it to the web page.
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
 * Initialize the hourly chart layout and content.
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
