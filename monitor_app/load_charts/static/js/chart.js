// threshold for alert triggering

var threshold = 1.0;

// initialized data at apge load
getValues();
getAlerts();	

// update automation. Refresh data every 10 s
$(document).ready(function(){
	setInterval("getValues();", 10000);
	setInterval("getAlerts();", 10000);
});

// AJAX GET values to populate chart then draw it.
function getValues() {
	$.get("/load_charts/get-charts/", function (data){ drawChart(data, threshold); });
};
// AJAX GET alert and current statistics.
function getAlerts() {
	$.get("/load_charts/get-stats/?threshold="+threshold.toFixed(2), function (data){ 
		var alertJson = JSON.parse(data);
		updateAlert(alertJson); 
		updateStats(alertJson); 
	});
};

// Update Statistics
function updateStats(stats){
	$('#stats').html('<li class="stats-temp">IP Address : '+stats.ip+' - Server is up for '+stats.uptime+' - '+stats.users+'</li>');

	$("#top-right-clock").html(stats.clock);
};

// Add alert or recover message. Shadows older messages.
function updateAlert(alertJson) {

	var firstListClass = $('ul#alert-list li:first').attr('class');
	switch (alertJson.alert){
		case 1: 
			// load average alert, if previous message was a recover, then pop an alert message
			if (firstListClass == "recover" || firstListClass == "initialMessage") {
				$(".initialMessage").remove();
				$("."+firstListClass).toggleClass("old", true);
				$("."+firstListClass).toggleClass("recover", false);
				$('#alert-list').prepend('<li class="error">High load generated an alert - '+alertJson.value.toFixed(2)+' : <b> load</b>, triggered at '+alertJson.time+'</li>');
			}
			break;
		case 0:
			// load average is back to normal, if previous message was an alert, then pop arecover message
			if (firstListClass == "error") {
				$("."+firstListClass).toggleClass("old", true);
				$("."+firstListClass).toggleClass("error", false);
				$('#alert-list').prepend('<li class="recover">Load is back to normal, at '+alertJson.time+' - load :'+alertJson.value.toFixed(2)+' - threshold :'+threshold.toFixed(2)+'</li>');
			}
			break;
	}
};
//format ECMA and ISO-8601. Needed to work with mozilla (rhino) and Safari
function format_date(date) {
	return new Date(date.split(' ').join('T')+'Z')
}

// D3. Call this function to redraw chart
function drawChart(values, alert) {

	d3.select(".chart").selectAll("*").remove();

	var data = JSON.parse(values);

	var height = 300,
		width = 610,
		margin = {top: 20, right: 10, bottom: 10, left: 50};

	var barWidth = 7;

	//return a rgb color where high load returns red and low load returns green
	var col = d3.scale.linear()
		.domain([Math.min(threshold, d3.min(data, function(d) { return d.value; })), d3.max(data, function(d) { return d.value; })])
		.range([0, 255]);

	var	currDate = format_date(data[0].date);
		minDate = d3.time.second.offset(d3.time.minute.offset(currDate, -10), -10);

	// x scale, based on time
	var x = d3.time.scale()
        .domain([minDate, currDate])
		.range([0, width]);

	// y scale
	var y = d3.scale.linear()
		.domain([0, Math.max(alert, d3.max(data, function(d) { return d.value; }))*1.05])
		.range([height, 0]);

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom");

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	//drag function for scrollable alert bar
	var drag = d3.behavior.drag()
		.origin(function() { 
  			var t = d3.select(this);
  			return {x: t.attr("x"), y: t.attr("y")};
  		})
        .on("drag", function(d, i) {
				var yPos = d3.event.y;
            d3.select(".thresholdText").attr("y", yPos)
            d3.select(".thresholdText").text("alert threshold: "+y.invert(yPos).toFixed(2));
            d3.select(".thresholdLine").attr("y", yPos)
            threshold = y.invert(yPos);
            })
       	.on("dragend", function(){ 
       		getAlerts(); 
       	});
            
    // chart funct
	var chart = d3.select(".chart")
	    .attr("width", width+margin.left+margin.right)
	    .attr("height", height+margin.top+margin.bottom);

	chart.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate("+margin.left+",0)")
		.call(yAxis)
	   .append("text")
	    .attr("transform", "rotate(-90)")
	    .attr("y", -45)
	    .attr("dy", ".71em")
	    .style("text-anchor", "end")
	    .text("Load");

	chart.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate("+margin.left+"," + height + ")")
		.call(xAxis);

	// for each eeent of data, draws corresponding rectangle coloured with col() funct
	chart.selectAll(".bar")
	    .data(data)
	  .enter().append("rect")
	  	.attr("fill", function(d){ return "rgb("+d3.round(col(d.value))+10+","+(255-d3.round(col(d.value)))+",0)";})
	  	.attr("class", "bar")
		.attr("x", function(d, i) { return x(format_date(d.date))+margin.left - barWidth/2; })
	  	.attr("width", barWidth)
		.attr("y", function(d) { return y(d.value); })
	    .attr("height", function(d) {return height - y(d.value); })
		.on("mouseover", function(d){ 
			$("#display-area").append('<p class="viewer"> <b>Time:</b> '+d.date.substr(d.date.length - 8)+'  -    <b>Load average over past minute :</b> '+d.value+'</p>'); })
		.on("mouseout", function(){ $(".viewer").remove(); });

	// alert line. You can drag it
	chart.append("rect")
		.attr("class", "thresholdLine")
		.attr("y",function() { return y(alert); })
		.attr("x",function() { return margin.left; })
		.attr("width", function(d) { return width+barWidth/2; })
		.attr("fill", "#111111")
		.attr("height", "1")
		.style("cursor", "ns-resize")
		.call(drag);

	// displays threshold
	chart.append("text")
		.attr("class", "thresholdText")
		.attr("y",function(d) { return y(alert); })
		.attr("dy", "-5")
		.attr("x",function(d,i) { return margin.left+93; })
		.text("alert threshold: "+alert.toFixed(2))
		.attr("fill", "#000")
		.style("cursor", "ns-resize")
		.call(drag);
};