from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@user.route("/course/getlist", methods=["GET"])
def userGetCourseList():
    user = User.query.get(getUserId())
    courseList = Course.query.all()
    return jsonify(OK(
        courselist=[
            {
                "courseid": course.course_id,
                "title": course.title,
                "is_collect": True if course in user.courses else False
            }
        for course in courseList]
    ))


@user.route("/course", methods=["GET"])
def userGetCourse():
    user = User.query.get(getUserId())
    courseId = request.args.get("courseid")
    if courseId is None:
        return jsonify(Error1002())
    course = Course.query.get(courseId)
    if course is None:
        return jsonify(Error1002())
    return jsonify(OK(
        course={
            "courseid": course.course_id,
            "title": course.title,
            # http://127.0.0.1:5000/file/download/courses/1.md
            "coursedetail": "http://" + current_app.config['HOST'] + "/file/download/courses/" + course.details,
            "is_collect": True if course in user.courses else False
        }
    ))


@user.route("/course/code")
def userGetCourseCode():
    courseId = request.args.get("courseid")
    codeList = Code.query.filter_by(course_id=courseId, is_show=True).all()
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


@user.route("/course/collect", methods=["POST"])
def userCollectCourse():
    userId = getUserId()
    user = User.query.get(userId)
    courseId = request.json.get("courseid")
    if courseId is None:
        return jsonify(Error1002())
    course = Course.query.get(courseId)
    if course is None:
        return jsonify(Error1002())
    if course not in user.courses:
        user.courses.append(course)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())


@user.route("/course/collect", methods=["DELETE"])
def userUnCollectCourse():
    userId = getUserId()
    user = User.query.get(userId)
    courseId = request.json.get("courseid")
    if courseId is None:
        return jsonify(Error1002())
    course = Course.query.get(courseId)
    if course is None:
        return jsonify(Error1002())
    if course in user.courses:
        user.courses.remove(course)
        db.session.commit()
        return jsonify(OK())
    else:
        return jsonify(Error1002())