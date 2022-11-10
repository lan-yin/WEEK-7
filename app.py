from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response, g
import mysql.connector
from mysql.connector import pooling
from flask_restful import Api, Resource
from flask_cors import CORS


poolname = "mysqlpool"
poolsize = 32
host = "localhost"
user = "root"
password = "root@2022"
database = "website"

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=poolname, pool_reset_session=True, pool_size=poolsize, host=host, user=user, password=password, database=database, charset="utf8mb4")
mydb = cnxpool.get_connection()
mycursor = mydb.cursor(buffered=True)
# mycursor = mydb.cursor()


class UserResponse(Resource):
    def get(self):
        if "username" in session:
            dictResponse = {"success": False, "info": "查詢失敗", "data":None}
            try:
                username = request.args.get("username")
                sql = "SELECT*FROM member WHERE username=%s"
                val = (username, )
                mycursor.execute(sql, val)
                if mycursor.rowcount > 0:
                    result = mycursor.fetchone()
                    data = {}
                    for i, row in enumerate(result):
                        key = mycursor.description[i][0]
                        data[key] = row
                    dictResponse["success"] = True
                    dictResponse["info"] = "查詢成功"
                    dictResponse["data"] = data
                else:
                    dictResponse["info"] = "無此用戶"
                mydb.commit()

            except Exception as e:
                mydb.rollback()
                dictResponse["info"] = f"SQL 執行失敗：{e}"
            
            return jsonify(dictResponse)
        else:
            return redirect("/")


    def patch(self):
        dictResponse = {"name": None}
        try:
            name = request.get_json()["name"]
            # username = "test6"
            username = session["username"]
            if username == None:
                return jsonify({"error": True})
            sql = "UPDATE member SET name=%s WHERE username=%s"
            val = (name, username, )
            mycursor.execute(sql, val)
            mydb.commit()
            session["name"] = name
            dictResponse["name"] = name
            dictResponse["ok"] = True
            # response = make_response(dictResponse)
            return jsonify(dictResponse)
            # return response
        except:
            return jsonify({"error": True})
        


app = Flask(__name__, static_folder="public", static_url_path="/")
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key = "noOneKnows"
api.add_resource(UserResponse, '/api/member')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/signup', methods=['POST', "GET"])
def signup():
    name = request.form["name"]
    user = request.form["user"]
    password = request.form["password"]

    sql = "SELECT username FROM member WHERE username = %s"
    val = (user,)
    mycursor.execute(sql, val)
    myResult = mycursor.fetchone()
    if myResult == None:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (name, user, password)
        mycursor.execute(sql, val)
        mydb.commit()
        session["username"] = user
        session["name"] = name
        return redirect("/member")

    else:
        return redirect("/error?message=帳號已經被註冊")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    user = request.form["user"]
    password = request.form["password"]
    if user == "" or password == "":
        return redirect("/error?message=帳號、或密碼輸入錯誤")

    sql = "SELECT username, password, name FROM member WHERE username = %s"
    val = (user,)
    mycursor.execute(sql, val)
    myResult = mycursor.fetchone()

    if myResult == None:
        return redirect("/error?message=帳號、或密碼輸入錯誤")

    if password == myResult[1]:
        session["username"] = user
        session["name"] = myResult[2]
        return redirect("/member")
    else:
        return redirect("/error?message=帳號、或密碼輸入錯誤")


@app.route("/member")
def member():
    if "username" in session:
        name = session["name"]
        return render_template("member.html", name=name)
    else:
        return redirect("/")


@app.route("/message", methods=["POST", "GET"])
def message():
    try:
        username = session["username"]
        message = request.form["mesg"]
    except:
        redirect("/error?message=請先登入會員")


@app.route("/error")
def error():
    try:
        mseg = request.args.get("message")
        return render_template("error.html", message=mseg)
    except:
        return redirect("/")


@app.route("/signout")
def signout():
    session.pop("username", None)
    session.pop("name", None)
    return redirect("/")


# 啟動網站伺服器
if __name__ == "__main__":
    app.run(port=3000, debug=True)
