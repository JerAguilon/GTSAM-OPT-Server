from flask import Flask, jsonify
from flask_restful import Resource, Api

from gtsam_example import planar2

app = Flask(__name__)
api = Api(app)


class SlamExample(Resource):
    def get(self):
        return planar2.run().serialize()

api.add_resource(SlamExample, '/')

if __name__ == '__main__':
    app.run(debug=True)
