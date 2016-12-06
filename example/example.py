from flask import Flask, render_template
from flask_googlecharts import GoogleCharts, BarChart


app = Flask(__name__)
charts = GoogleCharts(app)


@app.route("/")
@charts.include_charts
def index():
    hot_dog_chart = BarChart("hot_dog_chart", options={"title": "Contest Results",
                                                       "width": 640,
                                                       "height": 480})
    hot_dog_chart.add_column("string", "Competitor")
    hot_dog_chart.add_column("number", "Hot Dogs")
    hot_dog_chart.add_rows([["Matthew Stonie", 62],
                            ["Joey Chestnut", 60],
                            ["Eater X", 35.5],
                            ["Erik Denmark", 33],
                            ["Adrian Morgan", 31]])

    charts.register(hot_dog_chart)
    return render_template("index.html")

if __name__ == "__main__":

    app.run()