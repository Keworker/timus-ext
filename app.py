from typing import NoReturn as Unit

from flask_cors import CORS
from randomcolor import RandomColor
import requests
from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify

from auth import blueprint as auth_api
from friends import blueprint as friends_api
from problems import blueprint as problems_api
import db_session


app: Flask = Flask(__name__)
API_URL: str = "https://keworker.pythonanywhere.com/api/"
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


@app.route("/about")
def about() -> Unit:  # {
    """
    Handler for about page.
    :return: HTML page
    """
    return render_template(
        "about.html",
        title="About",
        static=url_for("static", filename=""),
        id=int(request.args["id"] if "id" in request.args else -1)
    )
# }


@app.route("/")
def baseUrl() -> Unit:  # {
    """
    Handler for base URL. Redirect to about page.
    :return: redirect
    """
    return redirect(
        "/about",
        308
    )
# }


@app.route("/problems")
def problems() -> Unit:  # {
    """
    Handler for problems page.
    :return: HTML page
    """
    if ("id" not in request.args):  # {
        return redirect("/auth")
    # }
    problemsDict = requests.get(f"{API_URL}problems?id={request.args['id']}").json()
    problemsForHtml: list = []
    colorRandomizer: RandomColor = RandomColor()
    id2color: dict = {}
    for it in problemsDict.keys():  # {
        id2color[it] = colorRandomizer.generate(luminosity="bright")[0]
    # }
    for problemId, params in problemsDict[list(problemsDict.keys())[0]]["problems"].items():  # {
        problemsForHtml.append(
            {
                "number": problemId,
                "name": params["name"],
                "url": params["url"],
                "solvers": [
                    {
                        "name": it["name"],
                        "color": id2color[curId]
                    } for curId, it in problemsDict.items()
                    if it["problems"][problemId]["solution_status"] == "accepted"
                ]
            }
        )
    # }
    return render_template(
        "problems.html",
        title="Problems",
        static=url_for("static", filename=""),
        id=int(request.args["id"]),
        problems=problemsForHtml
    )
# }


@app.route("/friends")
def friends() -> Unit:  # {
    """
    Handler for friends page.
    :return: HTML page
    """
    if ("id" not in request.args):  # {
        return redirect("/auth")
    # }
    return render_template(
        "friends.html",
        title="Friends",
        static=url_for("static", filename=""),
        id=int(request.args["id"]),
        api=API_URL,
        friends=requests.get(f"{API_URL}friends?id={request.args['id']}").json()
    )
# }


@app.route("/auth")
def auth() -> Unit:  # {
    """
    Handler for auth page.
    :return: HTML page
    """
    return render_template(
        "auth.html",
        title="Authorization",
        static=url_for("static", filename=""),
        id=-1,
        api=API_URL
    )
# }


if __name__ == '__main__':  # {
    db_session.global_init("db/database.sqlite")
    app.register_blueprint(auth_api)
    app.register_blueprint(friends_api)
    app.register_blueprint(problems_api)
    app.run()
# }
