$(document).ready(function() {
    $('select').material_select();
    $('.tooltipped').tooltip({delay: 30});
    $('.modal').modal();
  });

var G = new jsnx.DiGraph();
var nodes = ['A','B','C','D','E']
var w_edges = [['A','B',5], ['B','C',4], ['C','D',8], ['D','C',8], ['D','E',6], ['A','D',5], ['C','E',2], ['E','B',3], ['A','E',7]];
G.addNodesFrom(nodes);
G.addWeightedEdgesFrom(w_edges);

var defaultTrains;

// Draw our network graph as an SVG using D3.
// JSNetworkX handles most of the necessary translations to D3.
try {
    jsnx.draw(G, {
    element: '#viewGraph', 	// This is the only required option.
    withLabels: true,		// Label our nodes
    nodeStyle: {
      fill: function(d) {
        return d.data.color || '#AAA'; // any node without color is gray
      }
    }
  });
}
catch (err) {console.log(err);}

//$("#metric").change(function() {
//	  var selected = $('#metric :selected').val(); 
//	  if ( selected === '1') {
//		  $('#maxExact').val(0).addClass("disabled");
//		  $('#numberStops').text('').addClass("disabled");
//		  $('#distanceToGo').text('').addClass("disabled")
//	  }
//	  else {
//		  $('#maxExact').removeClass("disabled");
//		  $('#numberStops').text('').removeClass("disabled");
//		  $('#distanceToGo').text('').removeClass("disabled")
//	  }
//  
//});


var stations = [];

$(function () {
    $('a#getOutput').bind('click', function() {
    	stations.length = 0;
    	try {
    		if ($('#stations :selected').length > 1) {
	    		$('#stations > option:selected').each(function() {
	    			stations.push($(this).text());
	    		});
	    		getOutput();
	    	}
	    	else if ($('#randomStations').val()) {
	    		stations = $('#randomStations').val().toUpperCase().split(',');
	    		if(stations.length > 1) {
	    			// If more than 1 station has been entered by the user, loop through the stations to determine if any incorrect stations have been entered.
	    			var not_valid = 0;
	    			for (var i=0; i<stations.length;i++) {
	    			// If a station is not found iin our nodes array, increment the count of invalid stations by 1
	    				if (($.inArray(stations[i],nodes)) === -1) {
	    					not_valid++
	    				}
	    			}
	    			// If the number of invalid stations is more than 0, alert the user and return to the page
    				if (not_valid > 0) {
    					$('#modal2').modal('open');
    					$('#outputDiv').fadeOut('fast', function() { 
    						$('#outputDiv').html("<span class=white-text>Output</span>"); 
    						$('#outputDiv').fadeIn('fast'); 
    						});
    				}
    				else getOutput();
	    		}
	    		else $('#modal1').modal('open');
	    	}
	    	else { 
	    		$('#modal1').modal('open'); 
	    	}
    	}
    	// Log any errors to the console
    	catch (err) {
    		console.log(err);
    	}
    		
    });
});

function getOutput() {
	try {
		// Retrieve User selections and send to our python API "getOutput"
		// Get response and add it to our outputDiv
		var not_valid = 0;
		
		var data = { 	metric: $('#metric option:selected').val(),
						stations: stations,						
						maxexact: $('#maxExact option:selected').val() };
		// Check if the stops value entered was a positive number or left blank
		// If true, add the stops to the data to be sent. If not true, increment not_valid  by +
		if ( ($('#numberStops').val() > 0) || ($('#numberStops').val() === '')) {
			$.extend(data, {stops: $('#numberStops').val()});
		}
		else not_valid++
		
		// Check if the stops value entered was a positive number or left blank
		// If true, add the stops to the data to be sent. If not true, increment not_valid  by +
		if ( ($('#distanceToGo').val() > 0) || ($('#distanceToGo').val() === '')) {
			$.extend(data, {distance: $('#distanceToGo').val()});
		}
		else not_valid++
		if (not_valid > 0) {
			$('#modal3').modal('open');
		}
		else {
			$.getJSON("/getOutput", data,				
					function(response) {
						$('#outputDiv').fadeOut('fast', function() { 
						$('#outputDiv').html("<span class=white-text>" + response.result + "</span>"); 
						$('#outputDiv').fadeIn('fast'); 
						});
			    });	
		}
	}
	// Log any errors to the console
	catch (err) {
		console.log(err);
	}
}


