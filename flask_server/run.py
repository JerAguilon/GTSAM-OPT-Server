from flask import Flask
from flask_restful import Resource, Api
from webargs.flaskparser import use_args


from gtsam_example import planar2
from schemas.slam_example import PostSlamSchema
from models.example_input import SLAMRequest


class CustomApi(Api):
    def handle_error(self, e):
        if hasattr(e, 'code'):
            if e.code == 422 and 'messages' in e.data:
                data = e.data['messages']
                return self.make_response(data, 422)
        return self.make_response(e.data, 500)


app = Flask(__name__)

api = CustomApi(app)

class SlamExample(Resource):

    @use_args(
        PostSlamSchema(),
        locations=('json', 'form'),
    )
    def post(self, args):
        request = SLAMRequest.from_request(args)
        return planar2.run(request).serialize()

api.add_resource(SlamExample, '/')

if __name__ == '__main__':
    app.run(debug=True)
