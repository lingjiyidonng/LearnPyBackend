from app.user import user
from flask import request, jsonify, current_app
from app.model.response import *
from app.model.dbmodel import *
from app.utils.jwtutils import *
from datetime import date, timedelta


@user.route("/sign", methods=["GET"])
def userSign():
    user = User.query.get(getUserId())
    if len(user.signs) > 0 and user.signs[-1].date == date.today():
        pass
    else:
        sign = Sign(date=date.today(), user_id=user.user_id)
        db.session.add(sign)
        db.session.commit()
    datelist = [
        date.today() + timedelta(days=-3),
        date.today() + timedelta(days=-2),
        date.today() + timedelta(days=-1),
        date.today(),
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=2),
        date.today() + timedelta(days=3),
    ]
    res = []
    for day in datelist:
        temp = {
            "date": day.strftime("%d"),
            "week": day.strftime("%a"),
            "is_sign": False
        }
        if Sign.query.filter_by(user_id=user.user_id, date=day).first() is not None:
           temp["is_sign"] = True
        res.append(temp)
    return jsonify(OK(
        days=res,
        today=date.today().strftime("%Y-%m-%d %a")
    ))


