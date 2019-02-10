from flask import Flask
from flask_cors import CORS
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
        if hasattr(e, 'data'):
            return self.make_response(e.data, 500)
        return super(CustomApi, self).handle_error(e)


app = Flask(__name__)
CORS(app)

api = CustomApi(app)

class SlamExample(Resource):

    @use_args(
        PostSlamSchema(),
        locations=('json', 'form'),
    )
    def post(self, args):
        request = SLAMRequest.from_request(args)
        result = planar2.run(request).serialize()
        return result

api.add_resource(SlamExample, '/')

if __name__ == '__main__':
    app.run(debug=True)
