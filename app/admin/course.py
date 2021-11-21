from app.admin import admin
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@admin.route("/course/getlist")
def adminGetCourseList():
    courseList = Course.query.all()
    return jsonify(OK(
        courselist=[
            {
                "courseid": course.course_id,
                "title": course.title,
                "detail": "http://" + current_app.config['HOST'] + "/file/download/courses/" + course.details
            }
            for course in courseList
        ]
    ))


@admin.route("/course/update", methods=["PUT"])
def adminUpdateCourseList():
    courseId = request.json.get("courseid")
    detail = request.json.get("detail")
    course = Course.query.get(courseId)
    if course is None:
        return jsonify(Error1002())
    course.details = detail
    db.session.commit()
    return jsonify(OK())


@admin.route("/course/delete", methods=["DELETE"])
def adminDeleteCourse():
    pass