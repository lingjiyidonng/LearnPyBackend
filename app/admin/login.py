from app.admin import admin
from flask import request, jsonify
from app.model.dbmodel import *
from app.utils.jwtutils import getToken
from app.model.response import *


# 登录
@admin.route("/login", methods=["POST"])
def adminLogin():
    name = request.json.get("name")
    password = request.json.get("password")
    # 参数错误
    if name is None or password is None:
        return jsonify(Error1002())
    admin = Admin.query.filter_by(name=name).first()
    # 用户名不存在
    if admin is None:
        return jsonify(Error1002())
    # 密码错误
    if admin.checkPassword(password) is False:
        return jsonify(Error1001())
    token = getToken(admin.admin_id)
    return jsonify(OK(token=token))