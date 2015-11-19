function init() {
	$.get("/top").done(function(data) {
		data = JSON.parse(data);
		outputStr = "";
		for (var i in data)
			outputStr += "<tr><td><a href=\"http://www.reddit.com/r/"+data[i].f[0].v+"\">/r/"+data[i].f[0].v+"</a></td><td>"+data[i].f[1].v+"</td><td>"+data[i].f[2].v+"</td></tr>";
		$("#karmaFactories").append(outputStr);
	});
}