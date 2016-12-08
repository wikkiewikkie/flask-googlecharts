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

    def __init__(self, name, options=None, data_url=None):
        # type: (str, dict, str) -> None
        self.name = name
        self.options = options
        self.data_url = data_url

        self.parent = None

        self._columns = []
        self._rows = []

        if not isinstance(self.name, str):
            raise TypeError("name must be type str, not {}", type(self.name))
        if not self.name:
            raise ValueError("name must contain at least one character.")
        if " " in self.name:
            raise ValueError("name may not contain spaces; they are not supported in id values in HTML5.")
        if self.name[0] not in string.ascii_letters:
            raise ValueError("name must start with a lower or uppercase letter as it is used as a JavaScript \
            variable name")

    def add_column(self, type_, label=""):
        # type: (str, str) -> None
        if isinstance(label, str) and isinstance(type_, str):
            if type_ in ['boolean', 'date', 'datetime', 'number', 'string', 'timeofday']:
                self._columns.append((type_, label))
            else:
                raise ValueError("{} is not a valid column type".format(type_))
        else:
            raise TypeError("type_ and label must be strings")

    def add_rows(self, rows):
        # type: (list) -> None
        if isinstance(rows, list):
            self._rows += rows
        else:
            raise TypeError("rows must be type list, not {}".format(type(rows)))

    @property
    def data_json(self):
        return json.dumps(render_data(self._columns, self._rows))

    def html(self):
        return self.parent.templates['chart'].render(chart=self)

    @property
    def options_json(self):
        return json.dumps(self.options)


class AnnotationChart(GenericChart):
    class_ = "visualization"
    type_ = "AnnotationChart"
    package = "annotationchart"


class AreaChart(GenericChart):
    class_ = "visualization"
    type_ = "AreaChart"
    package = "corechart"


class BarChart(GenericChart):
    class_ = "visualization"
    type_ = "BarChart"
    package = 'corechart'


class BubbleChart(GenericChart):
    class_ = "visualization"
    type_ = "BubbleChart"
    package = "corechart"


class CalendarChart(GenericChart):
    class_ = "visualization"
    type_ = "Calendar"
    package = "calendar"


class CandlestickChart(GenericChart):
    class_ = "visualization"
    type_ = "CandlestickChart"
    package = "corechart"


class ColumnChart(GenericChart):
    class_ = "visualization"
    type_ = "ColumnChart"
    package = "corechart"


class ComboChart(GenericChart):
    class_ = "visualization"
    type_ = "ComboChart"
    package = "corechart"


class DiffChart(GenericChart):

    def __init__(self, name, options=None, data_url=None):
        raise NotImplementedError("DiffChart is not yet available in Flask-GoogleCharts")


class GanttChart(GenericChart):
    class_ = "visualization"
    type_ = "Gantt"
    package = "gantt"


class GaugeChart(GenericChart):
    class_ = "visualization"
    type_ = "Gauge"
    package = "gauge"


class GeoChart(GenericChart):
    class_ = "visualization"
    type_ = "GeoChart"
    package = "geochart"


class Histogram(GenericChart):
    class_ = "visualization"
    type_ = "Histogram"
    package = "corechart"


class LineChart(GenericChart):
    class_ = "visualization"
    type_ = "LineChart"
    package = 'corechart'


class Map(GenericChart):
    class_ = "visualization"
    type_ = "Map"
    package = "map"


class MaterialBarChart(GenericChart):
    class_ = "charts"
    type_ = "Bar"
    package = "bar"


class MaterialColumnChart(GenericChart):
    class_ = "charts"
    type_ = "Bar"
    package = "bar"


class MaterialLineChart(GenericChart):
    class_ = "charts"
    type_ = "Line"
    package = 'line'


class MaterialScatterChart(GenericChart):
    class_ = "charts"
    type_ = "Scatter"
    package = "scatter"


class OrgChart(GenericChart):
    class_ = "visualization"
    type_ = "OrgChart"
    package = "orgchart"


class PieChart(GenericChart):
    class_ = "visualization"
    type_ = "PieChart"
    package = 'corechart'


class Sankey(GenericChart):
    class_ = "visualization"
    type_ = "Sankey"
    package = "sankey"


class ScatterChart(GenericChart):
    class_ = "visualization"
    type_ = "ScatterChart"
    package = "corechart"

class GoogleCharts(object):

    def __init__(self, app=None):

        self.app = app

        self.charts = {}
        self.config = None
        self.template_env = None
        self.templates = {}

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        # type: (flask.Flask) -> bool
        """Initializes the extension against the app"""
        if isinstance(app, flask.Flask):
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
            return True
        raise TypeError("app must be type flask.Flask, not {}".format(type(app)))

    def template_variables(self):
        if self.charts:
            return {'charts_init': self._get_script_markup(), 'charts': self._get_charts_markup()}
        return {}

    def _after_request(self, resp):
        # type: (flask.Response) -> flask.Response
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

    @staticmethod
    def _get_static_init():
        return flask.send_file(pkg_resources.resource_stream("flask_googlecharts", "static/charts.init.js"),
                               attachment_filename="charts.init.js")

    def _get_script_markup(self):
        return flask.Markup(self.templates['init'].render(charts=self.charts,
                                                          config=self.config,
                                                          packages=self.packages(),
                                                          include_tags=True))

    def packages(self):
        """JSON representation of the chart packages to load"""
        packages = list(set([c.package for c in self.charts.values()]))
        return json.dumps(packages)

    def register(self, chart):
        # type: (GenericChart) -> bool
        """Registers a chart in the app"""
        if isinstance(chart, GenericChart):
            if chart.name not in self.charts:
                    chart.parent = self
                    self.charts[chart.name] = chart
                    return True
            raise KeyError("chart with this name already exists")
        raise TypeError("chart must be subclass of GenericChart, not {}".format(type(chart)))
