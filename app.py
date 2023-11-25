

import matplotlib
from flask import Flask, send_file, request, json
from io import BytesIO

from getDatas import getTrends, getShoppingTrends
from main import getTrendsGraph, getShoppingGraph

app = Flask(__name__)

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

getTrends()

@app.route("/graph", methods=["GET"])
def index():
    plt = getTrendsGraph()
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route("/shopping", methods=["POST"])
def shoping():
    params = request.get_json()
    if len(params) == 0:
        return 'No parameter'

    plt = getShoppingGraph(getShoppingTrends(params['keyword']))
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')


app.run(debug=True, port=8888)
