from app.admin import admin
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@admin.route("/code/check", methods=["POST"])
def adminCheckCode():
    codeId = request.json.get("codeid")
    code = Code.query.get(codeId)
    if code is None:
        return jsonify(Error1002())
    if code.is_show == True:
        return jsonify(Error1002())
    code.is_show = True
    db.session.commit()
    return jsonify(OK())


@admin.route("/code/check", methods=["DELETE"])
def adminUnCheckCode():
    codeId = request.json.get("codeid")
    code = Code.query.get(codeId)
    if code is None:
        return jsonify(Error1002())
    if code.is_show == False:
        return jsonify(Error1002())
    code.is_show = False
    db.session.commit()
    return jsonify(OK())


@admin.route("/code/getlist")
def adminGetCodeList():
    codeList = Code.query.filter_by(is_show=False, is_commit = True).all()
    return jsonify(OK(
        codelist=[
            {
                "codeid": code.code_id,
                "user_id": code.user_id,
                "username": code.user.user_name,
                "dt": code.dt,
                "problemid": code.problem_id,
                "courseid": code.course_id,
                "detail": "http://" + current_app.config['HOST'] + "/file/download/" + code.codepath
            }
        for code in codeList]
    ))