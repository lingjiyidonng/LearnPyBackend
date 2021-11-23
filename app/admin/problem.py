from app.admin import admin
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@admin.route("/problem/getlist")
def adminGetProblemList():
    problemList = Problem.query.all()
    return jsonify(OK(
        problemlist=[
            {
                "problemid": problem.problem_id,
                "question": problem.details,
                "hint": problem.hint,
                "level": problem.level,
                "reference_code": "http://" + current_app.config['HOST'] + "/file/download/problemcode/" + problem.reference_code,
            }
        for problem in problemList]
    ))


@admin.route("/problem/update", methods=["PUT"])
def adminUpdateProblemList():
    problemId = request.json.get("problemid")
    print(problemId)
    question = request.json.get("question")
    hint = request.json.get("hint")
    level = request.json.get("level")
    referenceCode = request.json.get("referencecode")
    problem = Problem.query.get(problemId)

    if problem is None:
        return jsonify(Error1002())
    if question is not None:
        problem.details = question
    if hint is not None:
        problem.hint = hint
    if level is not None:
        problem.level = int(level)
    if referenceCode is not None:
        problem.reference_code = referenceCode
    db.session.commit()
    return jsonify(OK())
