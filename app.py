from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response, g
import mysql.connector
from mysql.connector import pooling
from flask_restful import Api, Resource
from flask_cors import CORS


poolname = "mysqlpool"
poolsize = 32
host = "localhost"
user = "root"
password = ""
database = "website"

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=poolname, pool_reset_session=True, pool_size=poolsize, host=host, user=user, password=password, database=database, charset="utf8mb4")
mydb = cnxpool.get_connection()
mycursor = mydb.cursor(buffered=True)
# mycursor = mydb.cursor()


class UserResponse(Resource):
    def get(self):
        if "username" in session:
            dictResponse = {"data":None}
            try:
                username = request.args.get("username")
                sql = "SELECT id, name, username FROM member WHERE username=%s"
                val = (username, )
                mycursor.execute(sql, val)
                if mycursor.rowcount > 0:
                    result = mycursor.fetchone()
                    data = {}
                    for i, row in enumerate(result):
                        key = mycursor.description[i][0]
                        data[key] = row
                    dictResponse["data"] = data
                    mydb.commit()
                    return jsonify(dictResponse)
                else:
                    return jsonify(dictResponse)
            except Exception as e:
                return jsonify(dictResponse)
            
        else:         
            return jsonify({"data":None})


    def patch(self):
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
            return jsonify({"ok": True})
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
        return redirect("/error?message=?????????????????????")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    user = request.form["user"]
    password = request.form["password"]
    if user == "" or password == "":
        return redirect("/error?message=??????????????????????????????")

    sql = "SELECT username, password, name FROM member WHERE username = %s"
    val = (user,)
    mycursor.execute(sql, val)
    myResult = mycursor.fetchone()

    if myResult == None:
        return redirect("/error?message=??????????????????????????????")

    if password == myResult[1]:
        session["username"] = user
        session["name"] = myResult[2]
        return redirect("/member")
    else:
        return redirect("/error?message=??????????????????????????????")


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
        redirect("/error?message=??????????????????")


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


# ?????????????????????
if __name__ == "__main__":
    app.run(port=3000, debug=True)
