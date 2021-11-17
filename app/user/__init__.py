from flask import Blueprint, request, jsonify
from app.model.response import Error1001
from app.utils.jwtutils import checkToken

user = Blueprint('user', __name__)


# token验证
@user.before_request
def checkUserToken():
    # 非登录接口需要请求头的token认证
    if request.path != "/user/login":
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


import app.user.login
import app.user.course
import app.user.problem
import app.user.project
import app.user.sign
import app.user.code
import app.user.home