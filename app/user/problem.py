from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@user.route("/problem/getlist", methods=["GET"])
def userGetProblemList():
    problemList = Problem.query.all()
    userId = getUserId()
    return jsonify(OK(
        problemlist=[
            {
                "problemid": problem.problem_id,
                "level": problem.level,
                "is_solve": True if userId in [user.user_id for user in problem.users] else False
            }
        for problem in problemList]
    ))


@user.route("/problem", methods=["GET"])
def userGetProblem():
    problemId = request.args.get("problemid")
    if problemId is None:
        return jsonify(Error1002())
    problem = Problem.query.get(problemId)
    userId = getUserId()
    if problem is None:
        return jsonify(Error1002())
    return jsonify(OK(
        problem={
            "problemid": problem.problem_id,
            "question": problem.details,
            "hint": problem.hint,
            "level": problem.level,
            "reference_code": "http://" + current_app.config['HOST'] + "/file/download/problemcode/" + problem.reference_code,
            "is_solved": True if userId in [user.user_id for user in problem.users] else False
        }
    ))


@user.route("/problem/code")
def userGetProblemCode():
    problemId = request.args.get("problemid")
    codeList = Code.query.filter_by(problem_id=problemId, is_show=True).all()
    return jsonify(OK(
        codelist=[
            {
                "codeid": code.code_id,
                "describe": code.describe,
                "username": code.user.user_name,
                "avatar": code.user.avatar,
                "dt": code.dt
            }
        for code in codeList]
    ))


@user.route("/problem/solve", methods=["POST"])
def userSolveProblem():
    userId = getUserId()
    user = User.query.get(userId)
    problemId = request.json.get("problemid")
    if problemId is None:
        return jsonify(Error1002())
    problem = Problem.query.get(problemId)
    if problem is None:
        return jsonify(Error1002())
    if problem not in user.problems:
        user.problems.append(problem)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())


@user.route("/problem/solve", methods=["DELETE"])
def userUnSolveProblem():
    userId = getUserId()
    user = User.query.get(userId)
    problemId = request.json.get("problemid")
    if problemId is None:
        return jsonify(Error1002())
    problem = Problem.query.get(problemId)
    if problem is None:
        return jsonify(Error1002())
    if problem.problem_id in [problem_.problem_id for problem_ in user.problems]:
        user.problems.remove(problem)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())


