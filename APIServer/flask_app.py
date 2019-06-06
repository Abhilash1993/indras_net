# Indra API server
import os
from flask import Flask
from flask_restplus import Resource, Api
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

home_dir = os.getenv("HOME", "")
if __name__ == "__main__":
    # On local machines, use relative path
    dir = home_dir + "/Desktop/indras_net/"
else:
    # On the server, use absolute path
    dir = "/home/indrasnet/indras_net/"

with open(dir + "models/models.json") as file:
    models_db = json.loads(file.read())["models_database"]
    models_response = []
    for model in models_db:
        doc = ""
        if "doc" in model:
            doc = model["doc"]
        models_response.append({"name": model["name"], "doc": doc})


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/models')
class Models(Resource):
    def get(self):
        return models_response


@api.route('/models/<int:model_id>/props')
class Props(Resource):
    def get(self, model_id):
        try:
<<<<<<< HEAD
            with open(dir + "models/"
                      + models_database[model_id]["props"]) as file:
=======
            with open(dir + "models/" + models_db[model_id]["props"]) as file:
>>>>>>> ac8dc47c2a056430c0600a495fa5ce730d8f9ee9
                return json.loads(file.read())

        except KeyError:
            return {"Error": "Invalid model id " + str(model_id)}

    def put(self, model_id):
        try:
<<<<<<< HEAD
            with open(dir
                      + "models/"
                      + models_database[model_id]["props"]):
                return {
                    "questions": ["Question 1", "Question 2", "Question 3"]
                }
=======
            with open(dir + "models/" + models_db[model_id]["props"]):
                return {"questions": ["Question 1"]}
>>>>>>> ac8dc47c2a056430c0600a495fa5ce730d8f9ee9
        except KeyError:
            return {"Error": "Invalid model id " + str(model_id)}


# @api.route("/models/<int:question1>/<int:question2>/<float:question3>/props")
# class Props(Resource):
#     def get(self, question1, question2, question3):
#         try:
#             # Ask Professor!!!!!
#             ...
#             # executing the answers.
#         except KeyError:
#             return {"Error": "Out of range"}

#     def put(self, question1, question2, question3):
#         return {
#             "menu": ["Item 1", "Item 2", "Item 3"],
#             "grid_height": question1,
#             "grid_width": question2,
#             "density": question3,
#         }


# @api.route("/models/<int:menuitem_id>/menu")
# class Props(Resource):
#     def get(self, menuitem_id):
#         try:
#             # Ask Professor!!!!!
#             ...
#             # executing specific menu item
#         except KeyError:
#             return {"Error": "Invalid menu item id " + str(menuitem_id)}
#     def put(self, menuitem_id):
<<<<<<< HEAD
#         return {
#             "execute": menuitem_id,
#             "menu": ["Item 1", "Item 2", "Item 3"]
#         }
=======
#         return {"execute": menuitem_id, "menu":
    #             ["Item 1", "Item 2", "Item 3"]}
>>>>>>> ac8dc47c2a056430c0600a495fa5ce730d8f9ee9


# Ask Professor!!!!!
# @api.route('/models//menu')
# class Model(Resource):
<<<<<<< HEAD
#     def put(self, model_fid):
#         return {
#             "name": models_database[model_id]["name"],
#             "status": "Is running!",
#             "menu": ["Item 1", "Item 2", "Item 3"]
#         }
=======
#     def put(self, model_id):
#         return {"name": models_db[model_id]["name"],
#                 "status": "Is running!",
#                 "menu": ["Item 1", "Item 2", "Item 3"]
#                }
>>>>>>> ac8dc47c2a056430c0600a495fa5ce730d8f9ee9

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
