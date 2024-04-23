from flask import Flask, make_response, jsonify

from api.database import db_session
from auth import blueprint as auth_api
from friends import blueprint as friends_api
from problems import blueprint as problems_api

app: Flask = Flask(__name__)


@app.errorhandler(404)
def notFound(error):  # {
    return make_response(jsonify({"error": "Not found", "additional_info": error}), 404)
# }


if __name__ == '__main__':  # {
    db_session.global_init("api/db/database.sqlite")
    app.register_blueprint(auth_api)
    app.register_blueprint(friends_api)
    app.register_blueprint(problems_api)
    app.run(debug=True)
# }
