from flask import Blueprint, request, render_template, redirect, url_for
import hashlib

from sqlalchemy import or_, and_, not_

from apps.user.model import User
from exts import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    return render_template("user/index.html")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        user = User()
        user.username = username
        user.password = str(hashlib.sha1(password.encode("utf-8")).hexdigest())
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.login"))
    return render_template("user/register.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        sha_pwd = hashlib.sha1(password.encode("utf-8")).hexdigest()
        user_list = User.query.filter_by(username=name)
        for user in user_list:
            if user.password == sha_pwd:
                return redirect(url_for("user.center"))
        else:
            return render_template("user/login.html", msg="用户名或密码有误")
    return render_template("user/login.html")


@user_bp.route("/center")
def center():
    user_list = User.query.filter(User.is_delete == False).all()
    print(user_list)
    return render_template("user/center.html", users=user_list)


@user_bp.route("/delete", endpoint="delete")
def delete_user():
    user_id = request.args.get("id")
    target = User.query.get(user_id)
    ''' 逻辑删除
    target.is_delete = True
    '''
    # 物理删除
    db.session.delete(target)
    db.session.commit()
    return redirect(url_for("user.center"))


@user_bp.route("/update", endpoint="update", methods=["GET", "POST"])
def update_user():
    if request.method == "POST":
        new_username = request.form.get("username")
        new_phone = request.form.get("phone")
        user_id = request.form.get("id")
        user = User.query.get(user_id)
        user.username = new_username
        user.phone = new_phone
        db.session.commit()
        return redirect(url_for("user.center"))
    else:
        user_id = request.args.get("id")
        user = User.query.get(user_id)
        return render_template("user/update.html", user=user)


@user_bp.route("/select")
def select():
    # con_user = User.query.filter(or_(User.username.startswith("v"), User.username.contains("d"))).all()
    # select * from 表名 where username like 'v%' or username like '%d%'
    # con_user = User.query.filter(and_(User.username.contains("v"), User.ctime.__eq__("2021-07-01 20:28:55"))).all()
    # select * from User where username like '%v%' and ctime = '2021-07-01 20:28:55'
    # con_user = User.query.filter(not_(User.ctime == "2021-07-01 20:28:55"))
    # select * from User where ctime != "2021-07-01 20:28:55"
    # con_user = User.query.filter(User.phone.in_(['211212', '1234']))
    # select * from User where phone in ('211212', '1234')
    con_user = User.query.filter(User.age.between(12, 34))
    print(con_user)
    return render_template("user/select.html", users=con_user)
