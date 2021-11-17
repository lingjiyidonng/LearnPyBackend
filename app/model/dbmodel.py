from app.extension import db
from werkzeug.security import generate_password_hash, check_password_hash


UserCourseRelation = db.Table(
    'user_course_relation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.course_id'))
)


UserProblemRelation = db.Table(
    'user_problem_relation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.problem_id'))
)


UserProjectRelation = db.Table(
    'user_project_relation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'))
)


# 用户表
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(255))
    openid = db.Column(db.String(255), unique=True)
    ban = db.Column(db.String(20), default=False)
    signs = db.relationship("Sign", backref="user", cascade="all")  # 查看所有的签到记录
    codes = db.relationship("Code", backref="user", cascade="all")  # 查看所有提交的代码
    courses = db.relationship('Course', secondary=UserCourseRelation, back_populates='users', cascade="all")
    problems = db.relationship('Problem', secondary=UserProblemRelation, back_populates='users', cascade="all")
    projects = db.relationship('Project', secondary=UserProjectRelation, back_populates='users', cascade="all")


# 教程表
class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    details = db.Column(db.Text)
    users = db.relationship('User', secondary=UserCourseRelation, back_populates='courses', cascade="all")


# 题目表
class Problem(db.Model):
    __tablename__ = "problem"
    problem_id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)
    hint = db.Column(db.Text)
    reference_code = db.Column(db.Text)
    users = db.relationship('User', secondary=UserProblemRelation, back_populates='problems', cascade="all")


# 项目表
class Project(db.Model):
    __tablename__ = "project"
    project_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(255))
    users = db.relationship('User', secondary=UserProjectRelation, back_populates='projects', cascade="all")


# 管理员表
class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # 密码安全部分
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)


# 代码表
class Code(db.Model):
    __tablename__ = "code"
    code_id = db.Column(db.Integer, primary_key=True)
    is_show = db.Column(db.Boolean, default=False)
    code_details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    course_id = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)



# 签到表
class Sign(db.Model):
    __tablename__ = "sign"
    sign_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))