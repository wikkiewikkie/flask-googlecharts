function drawCharts() {

    $('.chart').each( function(i, c) {

        var chartType = c.getAttribute("data-chart-type");
        var chartObject = new google[c.getAttribute("data-chart-class")][chartType](c);
        var chartName = c.getAttribute('data-chart-name');
        var chartOptions = getChartOptions(chartName);
        var chartData = getChartData(c);
        if (c.getAttribute('data-chart-material')) {;
            chartObject.draw(chartData, google.charts[chartType].convertOptions(chartOptions));
        } else {
            chartObject.draw(chartData, chartOptions);
        }

    } );

}

function getChartOptions(n) {
    return JSON.parse($('#chart-options-' + n).text());
}

function getChartData(c) {
  var data = null;
  if ( c.getAttribute('data-chart-data-element') ) {
        data = JSON.parse($('#chart-data-' + c.getAttribute('data-chart-name')).text());
  } else if ( c.getAttribute('data-chart-data-url') ) {
        data = $.ajax({url: c.getAttribute('data-chart-data-url'), dataType: 'json', async: false}).responseText;
  }

  if (data) {
    return new google.visualization.DataTable(data);
  }

}