from flask import Flask, jsonify, render_template, url_for
from flask_googlecharts import GoogleCharts, BarChart, PieChart


app = Flask(__name__)
charts = GoogleCharts(app)


@app.route("/data")
def data():

    data = {"cols": [{"id": "", "label": "Topping", "pattern": "", "type": "string"},
                     {"id": "", "label": "Slices", "pattern": "", "type": "number"}],
            "rows": [{"c": [{"v": "Mushrooms", "f": None}, {"v": 3, "f": None}]},
                     {"c": [{"v": "Onions", "f": None}, {"v": 1, "f": None}]},
                     {"c": [{"v": "Olives", "f": None}, {"v": 1, "f": None}]},
                     {"c": [{"v": "Zucchini", "f": None}, {"v": 1, "f": None}]},
                     {"c": [{"v": "Pepperoni", "f": None}, {"v": 2, "f": None}]}]}

    return jsonify(data)


@app.route("/")
def index():
    hot_dog_chart = BarChart("hot_dogs", options={"title": "Contest Results",
                                                       "width": 300,
                                                       "height": 300})


    hot_dog_chart.add_column("string", "Competitor")
    hot_dog_chart.add_column("number", "Hot Dogs")
    hot_dog_chart.add_rows([["Matthew Stonie", 62],
                            ["Joey Chestnut", 60],
                            ["Eater X", 35.5],
                            ["Erik Denmark", 33],
                            ["Adrian Morgan", 31]])

    charts.register(hot_dog_chart)

    pizza_chart = PieChart("pizza",
                           options={"title": "Pizza Toppings",
                                    "width": 300,
                                    "height": 300},
                           data_url=url_for('data'))

    charts.register(pizza_chart)

    return render_template("index.html")

if __name__ == "__main__":

    app.run(debug=True)