from app.admin import admin
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


projectType = ["网络爬虫", "网络开发", "机器人", "数据科学", "机器学习", "OpenCV", "深度学习", "其他"]


@admin.route("/project/getlist")
def adminGetprojectList():
    res = {}
    for pty in projectType:
        res[pty] = [
            {
                "project": project.project_id,
                "projectname": project.name,
                "projecturl": project.url,
            }
            for project in Project.query.filter_by(type=pty).all()
        ]
    return jsonify(OK(res))


@admin.route("/project/update", methods=["PUT"])
def adminUpdateProjectList():
    projectId = request.json.get("projectid")
    print(projectId)
    name = request.json.get("name")
    url = request.json.get("url")
    project = Project.query.get(projectId)
    if project is None:
        return jsonify(Error1002())
    if name is not None:
        project.name = name
    if url is not None:
        project.hint = url
    db.session.commit()
    return jsonify(OK())