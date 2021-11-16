def OK(msg="", **kwargs):
    return {
        "status": 0,
        "msg": msg,
        "data": kwargs
    }


# 验证不通过
def Error1001():
    return {
        "status": 1001,
        "msg": "Unauthorized"
    }


# 验证不通过
def Error1002():
    return {
        "status": 1002,
        "msg": "请求参数错误"
    }