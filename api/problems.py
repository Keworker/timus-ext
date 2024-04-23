from flask import Blueprint, request, make_response, jsonify
from sqlalchemy.orm import Session

from api.database.db_session import create_session
from api.database.friendship import Friendship
from api.database.user import User
from api.timus_helper import getUsersProblemsDict, getUsername

blueprint: Blueprint = Blueprint(
    "problems_api",
    __name__
)


@blueprint.route("/api/problems", methods=["GET"])
def problems():  # {
    """
    Returns dict with problems of user and his friends.
    :return: flask response
    """
    userId: int = int(request.args.get("id"))
    dbSession: Session = create_session()
    result: dict = {}
    try:  # {
        for id_ in list(map(lambda it: it.recipient_id,
                            dbSession.query(Friendship)
                                     .filter(Friendship.sender_id == userId).all()
                            )) + [userId]:  # {
            timusId: int = dbSession.query(User).filter(User.id_ == id_).one().timus_id
            problemsDict: dict = getUsersProblemsDict(timusId)
            name: str = getUsername(timusId)
            result[timusId] = {
                "name": name,
                "count": sum(map(lambda it: it["solution_status"] == "accepted",
                                 problemsDict.values())),
                "problems": problemsDict
            }
        # }
    # }
    finally:  # {
        dbSession.close()
    # }
    return make_response(
        jsonify(result),
        200
    )
# }
