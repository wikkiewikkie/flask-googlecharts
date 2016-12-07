from flask import Flask, jsonify, render_template, url_for
from flask_googlecharts import GoogleCharts, BarChart, MaterialLineChart
from flask_googlecharts.utils import prep_data

import datetime

app = Flask(__name__)
charts = GoogleCharts(app)


@app.route("/data")
def data():

    d = {"cols": [{"id": "", "label": "Date", "pattern": "", "type": "date"},
                  {"id": "", "label": "Spectators", "pattern": "", "type": "number"}],
         "rows": [{"c": [{"v": datetime.date(2016, 5, 1), "f": None}, {"v": 3987, "f": None}]},
                  {"c": [{"v": datetime.date(2016, 5, 2), "f": None}, {"v": 6137, "f": None}]},
                  {"c": [{"v": datetime.date(2016, 5, 3), "f": None}, {"v": 9216, "f": None}]},
                  {"c": [{"v": datetime.date(2016, 5, 4), "f": None}, {"v": 22401, "f": None}]},
                  {"c": [{"v": datetime.date(2016, 5, 5), "f": None}, {"v": 24587, "f": None}]}]}

    return jsonify(prep_data(d))


@app.route("/")
def index():
    hot_dog_chart = BarChart("hot_dogs", options={"title": "Contest Results",
                                                  "width": 500,
                                                  "height": 300})

    hot_dog_chart.add_column("string", "Competitor")
    hot_dog_chart.add_column("number", "Hot Dogs")
    hot_dog_chart.add_rows([["Matthew Stonie", 62],
                            ["Joey Chestnut", 60],
                            ["Eater X", 35.5],
                            ["Erik Denmark", 33],
                            ["Adrian Morgan", 31]])

    charts.register(hot_dog_chart)

    spectators_chart = MaterialLineChart("spectators",
                                         options={"title": "Contest Spectators",
                                                  "width": 500,
                                                  "height": 300},
                                         data_url=url_for('data'))

    charts.register(spectators_chart)

    return render_template("index.html")

if __name__ == "__main__":

    app.run(debug=True)
