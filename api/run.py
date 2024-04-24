from flask import Flask, make_response, jsonify
from flask_cors import CORS

from api.auth import blueprint as auth_api
from api.friends import blueprint as friends_api
from api.problems import blueprint as problems_api
from api.database import db_session

app: Flask = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.errorhandler(404)
def notFound(*args):  # {
    """
    Handles 404 exception.
    :param args:
    :return: flask response
    """
    return make_response(jsonify({"error": "Not found", "additional_info": args}), 404)
# }


if __name__ == '__main__':  # {
    db_session.global_init("api/db/database.sqlite")
    app.register_blueprint(auth_api)
    app.register_blueprint(friends_api)
    app.register_blueprint(problems_api)
    app.run(port=5005)
# }
