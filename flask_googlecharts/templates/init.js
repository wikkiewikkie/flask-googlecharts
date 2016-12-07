<script type="text/javascript" src="/charts.init.js"></script>
<script type="text/javascript">
google.charts.load("{{ config['GOOGLECHARTS_VERSION'] }}", {'packages':{{ packages }}});
google.charts.setOnLoadCallback(drawCharts);
</script>
{% for name, chart in charts.items() %}
<script class="chart-options" id="chart-options-{{ name }}" type="application/json">{{ chart.options_json }}</script>
{% if not chart.data_url %}<script class="chart-data" id="chart-data-{{ name }}" type="application/json">{{ chart.data_json }}</script>{% endif %}{% endfor %}