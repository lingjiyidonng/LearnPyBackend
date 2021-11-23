from app.admin import admin
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@admin.route("/user/getlist")
def adminGetUserList():
    userList = User.query.all()
    return jsonify(OK(
        userlist=[
            {
                "userid": user.user_id,
                "username": user.user_name,
                "avatar": user.avatar,
                "codecount": len(user.codes),
                "isban": user.ban
            }
        for user in userList]
    ))


@admin.route("/user/ban", methods=["POST"])
def adminBanUser():
    userId = request.json.get("userid")
    user = User.query.get(userId)
    if user is None:
        return jsonify(Error1002())
    if user.ban is True:
        return jsonify(Error1002())
    user.ban = True
    db.session.commit()
    return jsonify(OK())


@admin.route("/user/ban", methods=["DELETE"])
def adminUnBanUser():
    userId = request.json.get("userid")
    user = User.query.get(userId)
    if user is None:
        return jsonify(Error1002())
    if user.ban is False:
        return jsonify(Error1002())
    user.ban = False
    db.session.commit()
    return jsonify(OK())