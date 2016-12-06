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
