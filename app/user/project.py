from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *

projectType = ["网络爬虫", "网络开发", "机器人", "数据科学", "机器学习", "OpenCV", "深度学习", "其他"]

@user.route("/project/getlist")
def userGetProjectList():
    user = User.query.get(getUserId())
    res = {}
    for pty in projectType:
        res[pty] = [
            {
                "project": project.project_id,
                "projectname": project.name,
                "projecturl": project.url,
                "is_collected": True if project in user.projects else False
            }
            for project in Project.query.filter_by(type=pty).all()
        ]
    return jsonify(OK(res))


@user.route("/project/collect", methods=["POST"])
def userCollectProject():
    userId = getUserId()
    user = User.query.get(userId)
    projectId = request.json.get("projectid")
    if projectId is None:
        return jsonify(Error1002())
    project = Project.query.get(projectId)
    if project is None:
        return jsonify(Error1002())
    if project in user.projects:
        return jsonify(Error1002())
    if project not in user.projects:
        user.projects.append(project)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())


@user.route("/project/collect", methods=["DELETE"])
def userUnCollectProject():
    userId = getUserId()
    user = User.query.get(userId)
    projectId = request.json.get("projectid")
    if projectId is None:
        return jsonify(Error1002())
    project = Project.query.get(projectId)
    if project is None:
        return jsonify(Error1002())
    if project in user.projects:
        user.projects.remove(project)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())