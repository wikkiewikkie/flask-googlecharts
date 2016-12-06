Flask-GoogleCharts
==================

Installation
------------

    $ easy_install Flask-GoogleCharts

or

    $ pip install Flask-GoogleCharts

Set Up
------

Google charts are controlled through a ``GoogleCharts`` instance::

    from flask import Flask
    from flask_googlecharts import GoogleCharts

    app = Flask(__name__)
    charts = GoogleCharts(app)

You may also set up the ``GoogleCharts`` instance later using the **init_app** method::

    charts = GoogleCharts()

    app = Flask(__name__)
    charts.init_app(app)


Creating Charts
----------------

Import a chart type and declare it in your view, and give it a name at a minimum::

    from flask_googlecharts import BarChart

    my_chart = BarChart("my_chart")

The name you declare will be used to access your chart in the template, and also to name the resulting JavaScript
variables and HTML tags, so it must start with a letter and not contain any spaces.

You can customize your chart by setting the ``options`` argument::

    my_chart = BarChart("my_chart", options={'title': 'My Chart'})


Adding Data to a Chart
----------------------

If you will be pulling JSON data from another endpoint in your application, just specify the url in the ``data_url``
argument::

    my_chart = BarChart("my_chart", options={'title': 'My Chart'}, data_url=url_for('data'))

You can also populate the chart using the ``addColumn`` and ``addRows`` methods on the chart::

    hot_dog_chart.add_column("string", "Competitor")
    hot_dog_chart.add_column("number", "Hot Dogs")
    hot_dog_chart.add_rows([["Matthew Stonie", 62],
                            ["Joey Chestnut", 60],
                            ["Eater X", 35.5],
                            ["Erik Denmark", 33],
                            ["Adrian Morgan", 31]])

Including Charts in Templates
-----------------------------

First, add the chart javascript to your template::

    <head>
        <meta charset="UTF-8">
        <title>Flask-GoogleCharts Example</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        {{ charts_init }}
    </head>

You must always include the Google Charts API loader on any pages that include charts.  If you will be populating your
charts with JSON data from another endpoint, you must also include jQuery.  When the application is running in debug
mode, ``GoogleCharts`` will log a warning if these dependencies are not met.

Add the chart HTML to your template::

    <body>
    {{ charts.my_chart }}
    </body>
