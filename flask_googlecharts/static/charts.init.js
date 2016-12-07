function drawCharts() {

    $('.chart').each( function(i, c) {

        var chartName = c.getAttribute('data-chart-name');
        var chartType = c.getAttribute("data-chart-type");
        var chartObject = new google[c.getAttribute("data-chart-class")][chartType](c);
        var chartOptions = JSON.parse($('#chart-options-' + chartName).text());
        var chartDataUrl = c.getAttribute('data-chart-data-url');

        if (c.getAttribute('data-chart-material')) {
            chartOptions = google.charts[chartType].convertOptions(chartOptions);
        }

        if (chartDataUrl) {
            chartObject.options = chartOptions;
            $.ajax({url: chartDataUrl,
                    context: chartObject}).done( function(d) {this.draw(new google.visualization.DataTable(d),
                                                                        this.options); } );
        } else if (c.getAttribute('data-chart-data-element')) {
            chartObject.draw(new google.visualization.DataTable(JSON.parse($('#chart-data-' + chartName).text())),
                             chartOptions);
        }

    } );

}
