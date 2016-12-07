# -*- coding: utf-8
"""
    flask_googlecharts
    ~~~~~~~~~~~~~~~~~~

    Google charts API support for Flask.
"""
from jinja2 import Environment, PackageLoader

from .utils import render_data
import flask
import json
import pkg_resources
import string


class GenericChart(object):

    def __init__(self, name: str, options: dict = {}, data_url: str = None):
        self.name = name
        self.options = options
        self.data_url = data_url

        self.parent = None

        self.package = 'corechart'
        self.charts_class = None
        self._columns = []
        self._rows = []

        if not self.name:
            raise ValueError("Chart name must contain at least one character.")
        if " " in self.name:
            raise ValueError("Chart name may not contain spaces as they are not supported in id values in HTML5.")
        if self.name[0] not in string.ascii_letters:
            raise ValueError("Chart name must start with a lower or uppercase letter as it is used as a JavaScript \
            variable name")

    def add_column(self, name: str, type_: str):
        self._columns.append((name, type_))

    def add_rows(self, rows: list):
        self._rows += rows

    @property
    def data_json(self):
        return json.dumps(render_data(self._columns, self._rows))

    def html(self):
        return self.parent.templates['chart'].render(chart=self)

    @property
    def options_json(self):
        return json.dumps(self.options)


class BarChart(GenericChart):

    def __init__(self, name: str, options: dict = {}, data_url: str = None):
        super().__init__(name, options, data_url)
        self.class_ = "visualization"
        self.type_ = "BarChart"


class LineChart(GenericChart):

    def __init__(self, name: str, options: dict = {}, data_url: str = None):
        super().__init__(name, options, data_url)
        self.class_ = "visualization"
        self.type_ = "LineChart"


class MaterialLineChart(GenericChart):

    def __init__(self, name: str, options: dict = {}, data_url: str = None):
        super().__init__(name, options, data_url)
        self.class_ = "charts"
        self.type_ = "Line"
        self.package = 'line'


class PieChart(GenericChart):

    def __init__(self, name: str, options: dict = {}, data_url: str = None):
        super().__init__(name, options, data_url)
        self.class_ = "visualization"
        self.type_ = "PieChart"


class GoogleCharts(object):

    def __init__(self, app=None):

        self.app = app

        self.charts = {}
        self.config = None
        self.template_env = None
        self.templates = {}

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app: flask.Flask):
        self.app = app
        self.config = app.config
        self.config.setdefault("GOOGLECHARTS_VERSION", "current")
        self.app.after_request(self._after_request)
        self.app.context_processor(self.template_variables)

        # establish route for static javascript
        self.app.add_url_rule("/charts.init.js", "charts_init_js", self._get_static_init)

        # initialize templates
        self.template_env = Environment(loader=PackageLoader('flask_googlecharts', 'templates'))
        self.templates['init'] = self.template_env.get_template("init.js")
        self.templates['chart'] = self.template_env.get_template("chart.html")



    def template_variables(self):
        if self.charts:
            return {'charts_init': self._get_script_markup(), 'charts': self._get_charts_markup()}
        return {}

    def _after_request(self, resp: flask.Response):
        """Cleans out the charts variable between requests.  If the application is running in debug mode it will also
        check to see if Javascript dependencies have been met and that all chart divs are included in templates.  If
        they are not, it will log a warning."""
        if self.app.debug and self.charts:
            resp_data = resp.get_data().decode()
            for x in ["loader.js", "jquery"]:
                if x not in resp_data:
                    self.app.logger.warning("{} script not included on template.".format(x))
            for x in self.charts.keys():
                if "data-chart-name=\"{}\"".format(x) not in resp_data:
                    self.app.logger.warning("Chart \"{}\" not included on template.".format(x))

        self.charts = {}
        return resp

    def _get_charts_markup(self):
        return {n: flask.Markup(c.html()) for n, c in self.charts.items()}

    def _get_static_init(self):
        return flask.send_file(pkg_resources.resource_stream("flask_googlecharts", "static/charts.init.js"))

    def __get_packages(self):
        packages = list(set([c.package for c in self.charts.values()]))
        return json.dumps(packages)

    def _get_script_markup(self):
        return flask.Markup(self.templates['init'].render(charts=self.charts,
                                                          config=self.config,
                                                          packages=self.__get_packages(),
                                                          include_tags=True))

    def register(self, chart):
        if chart.name not in self.charts:
            chart.parent = self
            self.charts[chart.name] = chart
        else:
            raise KeyError("A chart with this name already exists.")
