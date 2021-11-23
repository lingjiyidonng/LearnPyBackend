import app.setting
from app.user import user
from flask import request, jsonify
from app.model.dbmodel import *
from app.utils.jwtutils import getToken
from app.model.response import *
import requests


# 登录
@user.route("/login", methods=["POST"])
def userLogin():
    code = request.json.get("code")
    # avatar = request.json.get("avatar")
    # username = request.json.get("username")
    if code is None:
        return jsonify(Error1002())
    print(code)

    appID = app.setting.appID  # 开发者关于微信小程序的appID
    appSecret = app.setting.SECRET  # 开发者关于微信小程序的appSecret
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    response_data = requests.get(wx_login_api, params=req_params)  # 向API发起GET请求
    data = response_data.json()
    print(data)
    openID = data.get('openid')  # 得到用户关于当前小程序的OpenID
    # session_key = data['session_key']  # 得到用户关于当前小程序的会话密钥session_key
    if openID is None:
        return jsonify(Error1001())
    user = User.query.filter_by(openid=openID).first()
    if user is None:
        user = User(openid=openID, user_name="temp")
        db.session.add(user)
        db.session.commit()
    if user.ban == True:
        return jsonify(Error1001())

    token = getToken(userId=user.user_id)
    return jsonify(OK(token=token))