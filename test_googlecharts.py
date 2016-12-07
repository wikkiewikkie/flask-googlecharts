from __future__ import with_statement

import json
import sys

from flask import Flask
from flask_googlecharts import BarChart, GenericChart, GoogleCharts, LineChart, MaterialLineChart

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestGenericCharts(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self.charts = GoogleCharts(app)
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.app = None

    def test_addColumn(self):
        chart = GenericChart("test")
        chart.add_column("string", "myColumn")
        assert chart._columns[0][0] == "string" and chart._columns[0][1] == "myColumn"
        with self.assertRaises(ValueError):
            chart.add_column("", "")
        with self.assertRaises(TypeError):
            chart.add_column(1)

    def test_init(self):
        with self.assertRaises(ValueError):
            chart = GenericChart("")
        with self.assertRaises(ValueError):
            GenericChart("A B")
        with self.assertRaises(ValueError):
            GenericChart("3")
        with self.assertRaises(TypeError):
            chart = GenericChart(1)


class TestGoogleCharts(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self.charts = GoogleCharts(app)
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.app = None

    def test(self):
        assert "GOOGLECHARTS_VERSION" in self.app.config
        assert "charts_init_js" in [x.endpoint for x in self.app.url_map.iter_rules()]
        assert "drawCharts()" in self.client.get("/charts.init.js").data.decode("utf8")

    def test_init_app(self):
        with self.assertRaises(TypeError):
            self.charts.init_app(1)

    def test_packages(self):
        chart = BarChart("test01_bar")
        self.charts.register(chart)
        chart = LineChart("test01_line")
        self.charts.register(chart)
        chart1 = MaterialLineChart("test01_mline")
        self.charts.register(chart1)
        assert set(json.loads(self.charts.packages())) == set(["corechart", "line"])

    def test_register(self):
        chart = BarChart("test")
        self.charts.register(chart)
        assert 'test' in self.charts.charts

        chart2 = LineChart("test")
        with self.assertRaises(KeyError):
            self.charts.register(chart2)

        with self.assertRaises(TypeError):
            self.charts.register(1)

    def test_template_variables(self):
        assert self.charts.template_variables() == {}
        self.charts.register(BarChart("test"))
        assert "charts" in self.charts.template_variables()
        assert "test" in self.charts.template_variables()["charts"]


if __name__ == "__main__":
    unittest.main()
