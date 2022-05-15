from flask import *
app=Flask(__name__)
from src.dbconnection import *

@app.route('/login_code',methods=['post'])
def login_code():
    username=request.form['uname']
    password=request.form['pswd']
    query="select *from login where username=%s and password=%s and type='student'"
    value=(username,password)
    print(value)
    res=selectone(query,value)
    if res is None:
        return jsonify({"task":"invalid"})
    else:
        return jsonify({"task": 'valid','id':res[0]})
@app.route('/viewdep',methods=['post'])
def viewdep():
    qry="select*from department"
    res=androidselectallnew(qry)
    return jsonify(res)


@app.route('/viewcourse',methods=['post'])
def viewcourse():
    depid=request.form['did']
    qry="SELECT * FROM `course` WHERE `course`.`depid`=%s"
    res=androidselectall(qry,depid)
    return jsonify(res)

@app.route('/viewcamnotification',methods=['post'])
def viewcamnotification():
    id = request.form['lid']
    qry="select*from camnotification where sid=%s"
    res=androidselectall(qry,id)
    return jsonify(res)


@app.route('/viewprofile',methods=['post'])
def viewprofile():
    lid=request.form['uid']
    qry="select * from `student` where `student`.`loginid`=%s"
    res=androidselectall(qry,lid)
    print(res)
    return jsonify(res)


app.run(host="0.0.0.0",port=5000)