from flask import Blueprint, request, jsonify
from app.model.response import Error1001
from app.utils.jwtutils import checkToken

admin = Blueprint('admin', __name__)


# token验证
@admin.before_request
def checkAdminToken():
    # 非登录接口需要请求头的token认证
    if request.path != "/admin/login":
        authorization = request.headers.get('Authorization')
        if authorization is None:
            return jsonify(Error1001())
        if " " in authorization:
            tempList = authorization.split(" ")
            tokenHead = tempList[0]
            token = tempList[1]
            if tokenHead is None or tokenHead != "Bearer":
                return jsonify(Error1001())
            if token is None:
                return jsonify(Error1001())
            data = checkToken(token)
            if data is None:
                return jsonify(Error1001())
        else:
            return jsonify(Error1001())

import app.admin.login
import app.admin.course
import app.admin.problem
import app.admin.code
import app.admin.project
import app.admin.user
