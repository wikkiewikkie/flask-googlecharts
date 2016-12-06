# -*- coding: utf-8
"""
    flask_googlecharts
    ~~~~~~~~~~~~~~~~~~

    Google charts API support for Flask.
"""
from functools import wraps
from jinja2 import Environment, PackageLoader
import flask
import json


class GenericGoogleChart(object):

    def __init__(self, name: str, options: dict = None):
        self.name = name
        self.options = options
        self.package = 'corechart'
        self._columns = []
        self._rows = []

    def add_column(self, name: str, type_: str):
        self._columns.append((name, type_))

    def add_rows(self, rows: list):
        self._rows += rows

    def html(self):
        return "<div id='googlecharts-{}'></div>".format(self.name)

    @property
    def options_declaration(self):
        return json.dumps(self.options)

    @property
    def rows_declaration(self):
        return json.dumps(self._rows)


class LineGoogleChart(GenericGoogleChart):

    @property
    def js_declaration(self):
        return "googleCharts.{} = new google.visualization.LineChart(document.getElementById('googlecharts-{}'))".format(self.name, self.name)


class MaterialLineGoogleChart(GenericGoogleChart):

    def __init__(self, name: str, options: dict = None):
        super().__init__(name, options)
        self.package = 'line'

    @property
    def options_declaration(self):
        return "google.charts.Line.convertOptions({})".format(json.dumps(self.options))

    @property
    def js_declaration(self):
        return "googleCharts.{} = new google.charts.Line(document.getElementById('googlecharts-{}'))".format(self.name, self.name)


class PieGoogleChart(GenericGoogleChart):

    @property
    def js_declaration(self):
        return "googleCharts.{} = new google.visualization.PieChart(document.getElementById('googlecharts-{}'))".format(self.name, self.name)


class BarGoogleChart(GenericGoogleChart):

    @property
    def js_declaration(self):
        return "googleCharts.{} = new google.visualization.BarChart(document.getElementById('googlecharts-{}'))".format(self.name, self.name)


class GoogleCharts(object):

    def __init__(self, app=None):

        self.app = app

        self.charts = {}
        self.config = None
        self.template_env = None

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app: flask.Flask):
        self.app = app
        self.config = app.config
        self.config.setdefault("GOOGLECHARTS_VERSION", "current")
        self.app.context_processor(self.template_variables)
        self.template_env = Environment(loader=PackageLoader('flask_googlecharts', 'templates'))

    def template_variables(self):
        return {'googlecharts_js': self._get_script_markup(), 'googlecharts': self._get_charts_markup()}

    def _get_charts_markup(self):
        return {n: flask.Markup(c.html()) for n, c in self.charts.items()}

    def __get_packages(self):
        packages = list(set([c.package for c in self.charts.values()]))
        return json.dumps(packages)

    def _get_script_markup(self):
        template = self.template_env.get_template("init.js")
        return flask.Markup(template.render(charts=self.charts,
                                            config=self.config,
                                            packages=self.__get_packages()))

    def generate_html(self):
        pass

    def include_charts(self, f):
        """Decorator"""
        @wraps(f)
        def decorated(*args, **kwargs):
            resp = flask.make_response(f(*args, **kwargs))
            return f(*args, **kwargs)
        return decorated

    def register(self, chart):
        self.charts[chart.name] = chart
