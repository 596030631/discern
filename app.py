import argparse
import datetime
import os
from os import urandom

from flask import Flask, render_template, request, jsonify, session, send_file, send_from_directory

import config
import loginUtils
import tqUtils
from database import get_connection
from main import load_model

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = urandom(50)
app.permanent_session_lifetime = datetime.timedelta(seconds=60 * 60)

IMG_PATH = 'img'

parser = argparse.ArgumentParser()
parser.add_argument('--cfg', default='models/v8/yolov8.yaml', help='Input your model yaml.')
parser.add_argument('--weights', default=str('weights/yolov8n.pt'), help='Path to input weights.')
args = parser.parse_args()
detect_model = load_model(args)


def execute_sql(sql):
    conn, curses = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route("/upload", methods=['POST'])
def uploadFile():
    # 保存文件的路径
    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('TPMService')[0], IMG_PATH)
    # 获取文件
    attfile = request.files.get('file')
    attfile.save(os.path.join(save_path, attfile.filename))
    url = attfile.filename
    predict = detect_model.predict(os.path.join(save_path, attfile.filename), None)
    category = []
    for i in predict['bbox']:
        category.append({'label':i['info']['category'], 'value':i['info']['category']})
    ret = {"code": 200, "category": category, "url": url, "message": "类别检测完成"}
    print(ret)
    return ret

@app.route('/download')
def download():
    file_name = request.args.get('file_name')
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), IMG_PATH)
    print(path)
    print(IMG_PATH)
    print(file_name)
    return send_from_directory(path, file_name)


@app.route("/detect", methods=['POST'])
def detect():
    data = request.get_json()
    print(f'识别入参:{data}')
    # 获取文件
    filename = data.get("name")
    category = data.get("category")

    # 保存文件的路径
    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('TPMService')[0], IMG_PATH, filename)

    predict = detect_model.predict(save_path, category)


    sql = f"""
                                       REPLACE INTO `pm` ( `jg`, `datetime`)
                                       VALUES ('{category}', '{datetime.datetime.now()}')
                                   """

    execute_sql(sql)
    ret = {"code": 200, "url": predict['url'], "message": "识别成功", "data": predict['bbox']}
    print(ret)
    return ret


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
