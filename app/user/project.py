from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *


@user.route("/project/getlist")
def userGetProjectList():
    pass