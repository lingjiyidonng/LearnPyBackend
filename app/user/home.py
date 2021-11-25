from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@user.route("/home/course", methods=["GET"])
def userCourseList():
    user = User.query.get(getUserId())
    return jsonify(OK(
        courses=[
            {
                "courseid": course.course_id,
                "title": course.title,
            }
        for course in user.courses]
    ))


@user.route("/home/project", methods=["GET"])
def userProjectList():
    user = User.query.get(getUserId())
    return jsonify(OK(
        projects=[
            {
                "projectid": project.project_id,
                "name": project.name,
                "url": project.url
            }
        for project in user.projects]
    ))


@user.route("/home/code", methods=["GET"])
def userCodeList():
    user = User.query.get(getUserId())
    return jsonify(OK(
        codes=[
            {
                "codeid": code.code_id,
                "describe": code.describe,
                "dt": code.dt
            }
        for code in user.codes]
    ))