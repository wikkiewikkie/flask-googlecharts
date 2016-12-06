<script type="text/javascript">

google.charts.load("{{ config['GOOGLECHARTS_VERSION'] }}", {'packages':{{ packages }}});

google.charts.setOnLoadCallback(drawGoogleCharts);

function drawGoogleCharts() {

    var googleCharts = {};
    var googleChartsData = {};
    var googleChartsOptions = {};

    {% for name, chart in charts.items() %}
    {% if chart._columns|count > 0 %}
    googleChartsData.{{ name }} = new google.visualization.DataTable();
        {% for column in chart._columns %}
    googleChartsData.{{ name }}.addColumn('{{ column[0] }}', '{{ column[1] }}');
        {% endfor %}
    googleChartsData.{{ name }}.addRows({{ chart.rows_declaration }});
    {% else %}
    {{ chart.data_declaration }};
    {% endif %}
    {% endfor %}



    {% for name, chart in charts.items() %}googleChartsOptions.{{ name }} = {{ chart.options_declaration }};
    {% endfor %}

    {% for name, chart in charts.items() %}{{ chart.js_declaration }};
    {% endfor %}

    for (gc in googleCharts) {
        googleCharts[gc].draw(googleChartsData[gc], googleChartsOptions[gc]);
    }

}
</script>