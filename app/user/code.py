import MySQLdb

from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *
import os
from app.setting import UPLOAD_PATH
from app.utils.codeutils import *
import datetime


@user.route("/code/run", methods=["POST"])
def userRunCode():
    user = User.query.get(getUserId())
    codeFile = request.json.get("codefile")
    if codeFile is None or os.path.exists(os.path.join(UPLOAD_PATH, codeFile)) is None:
        return jsonify(Error1002())

    # codeCommitCount = Code.query.filter(
    #     Code.user_id == user.user_id,
    #     datetime.datetime.now() - Code.dt <= datetime.timedelta(1/24/60)
    # ).count()
    # if codeCommitCount > 3:
    #     return jsonify(Error1002())

    code = Code(codepath=codeFile, user_id=user.user_id)
    db.session.add(code)
    db.session.commit()
    codeHandler = CodeHandler(codeFile)
    codeHandler.run()
    return jsonify(OK(
        codeid=code.code_id,
        res=codeHandler.res
    ))


@user.route("/code/commit", methods=["POST"])
def userCommitCode():
    user = User.query.get(getUserId())
    codeId = request.json.get("codeid")
    courseId = request.json.get("courseid")
    problemId = request.json.get("problemid")
    describe = request.json.get("describe")
    username = request.json.get("username")
    avatar = request.json.get("avatar")
    code = Code.query.get(codeId)
    course = Course.query.get(courseId)
    problem = Problem.query.get(problemId)
    if code is None or (course is None and problem is None) or (course is not None and problem is not None)\
            or username is None or avatar is None:
        return jsonify(Error1002())
    if course:
        code.course_id = course.course_id
    if problem:
        code.problem_id = problem.problem_id
    code.is_commit = True
    code.describe = describe
    user.avatar = avatar
    user.user_name = username
    db.session.commit()
    return jsonify(OK(codeid=code.code_id))


@user.route("/code/getcode")
def userGetCode():
    codeId = request.args.get("codeid")
    code = Code.query.get(codeId)
    if code is None:
        return jsonify(Error1002())
    return jsonify(OK(
        code={
            "codeid": code.code_id,
            "codefile": "http://" + current_app.config['HOST'] + "/file/download/" + code.codepath,
            "describe": code.describe,
            "is_commit": code.is_commit,
            "is_show": code.is_show,
            "dt": code.dt
        }
    ))