from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from api.database.db_session import create_session
from api.database.user import User
from api.timus_helper import userExist

blueprint: Blueprint = Blueprint(
    "auth_api",
    __name__
)


@blueprint.route("/api/auth", methods=["POST"])
def auth():  # {
    """
    Endpoint for authorisation. Allows only POST method.
    :return: flask response
    """
    dbSession: Session = create_session()
    try:  # {
        user = dbSession.query(User).filter(User.timus_id == request.json["timus_id"]).one()
        return make_response(
            jsonify(user.to_dict()),
            200
        )
    # }
    except NoResultFound:  # {
        if (userExist(request.json["timus_id"])):  # {
            user = User()
            user.timus_id = request.json["timus_id"]
            dbSession.add(user)
            dbSession.commit()
            return make_response(
                jsonify(user.to_dict()),
                201
            )
        # }
        return make_response(
            jsonify({"error": "No such user."}),
            404
        )
    # }
    finally:  # {
        dbSession.close()
    # }
# }
