from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from api.database.db_session import create_session
from api.database.friendship import Friendship
from api.database.user import User
from api.timus_helper import getUsername, userExist

blueprint: Blueprint = Blueprint(
    "friends_api",
    __name__
)


def __createUserIfNotExist(timusId: int, dbSession: Session) -> int:  # {
    try:  # {
        return dbSession.query(User).filter(User.timus_id == timusId).one().id_
    # }
    except NoResultFound:  # {
        user = User()
        user.timus_id = timusId
        dbSession.add(user)
        dbSession.commit()
        return user.id_
    # }
# }


def __getFriends(userId: int):  # {
    dbSession: Session = create_session()
    try:  # {
        return make_response(
            jsonify(
                [
                    {
                        "id": it.recipient_id,
                        "name": getUsername(
                            dbSession.query(User).filter(User.id_ == it.recipient_id).one().timus_id
                        )
                    } for it in dbSession.query(Friendship).filter(Friendship.sender_id == userId)
                ]
            ),
            200
        )
    # }
    finally:  # {
        dbSession.close()
    # }
# }


def __addFriend(userId: int, friendId: int):  # {
    if (userExist(friendId)):  # {
        dbSession: Session = create_session()
        try:  # {
            friendship = Friendship()
            friendship.sender_id, friendship.recipient_id = userId, \
                __createUserIfNotExist(friendId, dbSession)
            dbSession.add(friendship)
            dbSession.commit()
            return make_response(
                jsonify(
                    {
                        "id": friendship.recipient_id,
                        "name": getUsername(friendId)
                    }
                ),
                201
            )
        # }
        finally:  # {
            dbSession.close()
        # }
    # }
    else:  # {
        return make_response(
            jsonify({"error": "No such user."}),
            404
        )
    # }
# }


def __deleteFriend(userId: int, friendId: int):  # {
    dbSession: Session = create_session()
    try:  # {
        dbSession.execute(Friendship.__table__.delete()
                          .where(and_(Friendship.sender_id == userId,
                                      Friendship.recipient_id == friendId)))
        dbSession.commit()
        return make_response(jsonify({"status": "ok"}), 200)
    # }
    finally:  # {
        dbSession.close()
    # }
# }


@blueprint.route("/api/friends", methods=["GET", "POST", "DELETE"])
def friends():  # {
    """
    Endpoint to get, post or delete friends.
    :return: flask response
    """
    match request.method:  # {
        case "GET":  # {
            return __getFriends(int(request.args.get("id")))
        # }
        case "POST":  # {
            return __addFriend(int(request.args.get("id")), request.json["friend_timus_id"])
        # }
        case "DELETE":  # {
            return __deleteFriend(int(request.args.get("id")), request.json["id"])
        # }
    # }
# }
