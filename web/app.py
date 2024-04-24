from typing import NoReturn as Unit

from randomcolor import RandomColor
import requests
from flask import Flask, render_template, url_for, redirect, request

app: Flask = Flask(__name__)
API_URL: str = "http://127.0.0.1:5005/api/"


@app.route("/about")
def about() -> Unit:  # {
    return render_template(
        "about.html",
        title="About",
        static=url_for("static", filename=""),
        id=int(request.args["id"] if "id" in request.args else -1)
    )
# }


@app.route("/")
def baseUrl() -> Unit:  # {
    return redirect(
        "/about",
        308
    )
# }


@app.route("/problems")
def problems() -> Unit:  # {
    if ("id" not in request.args):  # {
        return redirect("/auth")
    # }
    problemsDict = requests.get(f"{API_URL}problems?id={request.args['id']}").json()
    problemsForHtml: list = []
    colorRandomizer: RandomColor = RandomColor()
    id2color: dict = dict()
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
    return render_template(
        "auth.html",
        title="Authorization",
        static=url_for("static", filename=""),
        id=-1,
        api=API_URL
    )
# }


if __name__ == '__main__':  # {
    app.run(debug=True)
# }
