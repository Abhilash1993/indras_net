
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask_restplus import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    # On local machines, use relative path
    dir = ""
else:
    # On the server, use absolute path
    dir = "/home/indrasnet/indras_net/"

with open(dir + "models/models.json") as file:
    models_database = json.loads(file.read())["models_database"]
    models_response = []
    for model in models_database:
        doc = ""
        if "doc" in model:
            doc = model["doc"]
        models_response.append(
                               {"name": model["name"],
                                "doc": doc})


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/models')
class Models(Resource):
    def get(self):
        response =  models_response
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@api.route('/models/<int:model_id>/props')
class Props(Resource):
    def get(self, model_id):
        try:
            with open(dir + "IndrasNetFlask/" +
                      models_database[model_id]["props"]) as file:
                return json.loads(file.read())

        except KeyError:
            return {"Error": "Invalid model id " + str(model_id)}


@api.route('/models/<int:model_id>/run')
class Model(Resource):
    def put(self, model_id):
        return {"name": models_database[model_id]["name"],
                "status": "Is running!"}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
