import matplotlib
from flask import Flask, send_file, request, json
from io import BytesIO

from flask_cors import CORS

from getDatas import getTrends, getShoppingTrends, trends
from main import getTrendsGraph, getShoppingGraph, train_and_evaluate_model

app = Flask(__name__)
CORS(app)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

getTrends()

cache = dict()
cacheShopping = dict()


@app.route("/graph", methods=["GET"])
def index():
    plt = getTrendsGraph()
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route("/graphlist", methods=["GET"])
def index2():
    a = set()
    for i in trends.values():
        a.update(i)
    return json.dumps(list(a), ensure_ascii=False)



@app.route("/shopping", methods=["GET"])
def shoping():
    params = request.args.getlist('keyword')
    if len(params) == 0 or len(params) > 5:
        return 'No parameter'
    print(params)
    a = getShoppingTrends(params)
    plt = getShoppingGraph(a)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route("/train", methods=["GET"])
def train():
    params = request.args.get('keyword')

    if len(params) == 0 or len(params) > 5:
        return 'No parameter'
    print(params)
    if params in cache:
        plt = cache[params][1]
    else:
        cache[params] = train_and_evaluate_model(getShoppingTrends([params])['results'][0])
        plt = cache[params][1]
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route("/train2", methods=["GET"])
def train2():
    params = request.args.get('keyword')
    if len(params) == 0 or len(params) > 5:
        return 'No parameter'
    print(params)
    if params in cache:
        scope = cache[params][0]
    else:
        cache[params] = train_and_evaluate_model(getShoppingTrends([params])['results'][0])
        scope = cache[params][0]
    advice = ""
    print(cache)
    if scope < -1:
        advice = "매우 위험"
    elif scope > 1:
        advice = "매우 안전"
    elif scope < -0.5:
        advice = "위험"
    elif scope > 0.5:
        advice = "안전"
    elif scope < 0:
        advice = "보통- 위험"
    elif scope > 0:
        advice = "보통- 안전"
    else:
        advice = "보통"
    return advice


app.run(debug=True, port=8888)
