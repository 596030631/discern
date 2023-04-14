import datetime

from flask import Flask, render_template, request, jsonify, Response, session
import time
import loginUtils
import utils, tqUtils, config
import string
from os import urandom
import joblib
import json
import tablib

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = urandom(50)
app.permanent_session_lifetime = datetime.timedelta(seconds=60 * 60)


@app.route("/tqyc")
def report():
    return render_template("tqyc.html")


@app.route('/')
def index():
    return render_template('index.html')



def generate_csv_data(data: dict) -> str:

    # Defining CSV columns in a list to maintain
    # the order
    csv_columns = data.keys()

    # Generate the first row of CSV
    csv_data = ",".join(csv_columns) + "\n"

    # Generate the single record present
    new_row = list()
    for col in csv_columns:
        new_row.append(str(data[col]))

    # Concatenate the record with the column information
    # in CSV format
    csv_data += ",".join(new_row) + "\n"

    return csv_data
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/ycxz')
def ycxz():
    return render_template('ycxz.html')




@app.route('/pm')
def pm():
    return render_template('pm.html')







@app.route("/findAll")
def findAll():
    data = tqUtils.findAll()
    return jsonify({"status": True, "msg": "查询所有信息成功", "data": data})

@app.route("/findPmAll")
def findPmAll():
    data = tqUtils.findPmAll()
    return jsonify({"status": True, "msg": "查询所有信息成功", "data": data})


@app.route("/tqByTime")
def tqByTime():
    content = request.args.get("content")
    startTime = request.args.get("startTime")
    endTime = request.args.get("endTime")
    data = tqUtils.tqByTime(content, startTime, endTime)
    return jsonify({"status": True, "msg": "查询所有信息成功", "data": data})


# 注册
@app.route("/register", methods=["POST", "GET"])
def register():
    # 获取注册信息
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    # 判断是否已经注册
    if loginUtils.is_registered(username, email):
        return jsonify({"status": False, "msg": "该用户已经注册"})
    # 注册
    if loginUtils.register(username, email, password):
        return jsonify({"status": True, "msg": "注册成功"})


# 登录
@app.route("/login", methods=["POST", "GET"])
def login():
    # 获取登录信息
    email = request.args.get("email")
    password = request.args.get("password")
    # 判断用户名密码是否正确
    if loginUtils.login(email, password):
        session['email'] = email
        session.permanent = True
        return jsonify({"status": True, "msg": "登录成功"})
    else:
        return jsonify({"status": False, "msg": "用户名或密码错误"})









# 退出登录
@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return render_template('index.html')

# 获取用户名
@app.route("/getUsername")
def getUsername():
    email = session.get('email')
    if email:
        username = loginUtils.getUser(email)
        return jsonify({"status": True, "data": username})





if __name__ == '__main__':
    app.run(debug=True)
