import csv
import matplotlib.pyplot as plt
import matplotlib
from flask import Flask, send_file
from io import BytesIO

from main import asdf

app = Flask(__name__)

matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

@app.route("/graph", methods=["GET"])
def index():
    plt = asdf()
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route("/csv", methods=["GET"])
def api():
    return "asdf"

app.run(debug=True, port=8888)