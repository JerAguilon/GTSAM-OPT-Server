from flask import Flask, jsonify

from gtsam_example import planar2

app = Flask(__name__)

@app.route('/')
def gtsam():
    return jsonify(planar2.run().serialize())
