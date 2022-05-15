import os
from flask import *
from werkzeug.utils import secure_filename

app=Flask(__name__)
from src.dbconnection import *
app.secret_key="123"
import functools
def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "id" not in session:
            return redirect ("/")
        return func()
    return secure_function


@app.route('/')
def start():
    return render_template('login.html')

@app.route('/add_course',methods=['get','post'])
@login_required
def add_course():
    qry="SELECT * FROM `department`"
    res=selectall(qry)
    return render_template('Add course.html',val=res)

@app.route('/adding_course',methods=['post'])
@login_required
def adding_course():
    dept=request.form['select']
    cor=request.form['textfield']
    qry="insert into course values(null,%s,%s)"
    value=(cor,dept)
    iud(qry,value)
    return '''<script>alert("Successfully added");window.location='/manage_course'</script>'''

@app.route('/add_department',methods=['post'])
@login_required
def add_department():
    return render_template('Add department.html')

@app.route('/department_name',methods=['post'])
@login_required
def department_name():
    dep=request.form['textfield']
    qry="insert into department values(null,%s)"
    value=dep
    iud(qry,value)
    return '''<script>alert("Successfully added");window.location='/manage_department'</script>'''

@app.route('/add_Hod',methods=['post'])
@login_required
def add_Hod():
    qry="select * from department"
    res=selectall(qry)
    return render_template('Add Hod.html',value=res)

@app.route('/add_staff',methods=['post'])
@login_required
def add_staff():
    qry="select *from department"
    res=selectall(qry)
    return render_template('Add staff.html',value=res)







@app.route('/staff_adding',methods=['post'])
@login_required
def staff_adding():
    try:

        Fn=request.form['textfield']
        Ln=request.form['textfield2']
        Gen=request.form['radiobutton']
        place=request.form['textfield3']
        post=request.form['textfield4']
        pin=request.form['textfield5']
        email=request.form['textfield6']
        quali=request.form.getlist('checkbox')
        qs=str.join(',',quali)
        dep=request.form['select']
        un=request.form['textfield7']
        pswd=request.form['textfield8']


        qry="insert into login values(null,%s,%s,'staff')"
        value=(un,pswd)
        id=iud(qry,value)
        qry1="insert into staff values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value1=(id,Fn,Ln,Gen,place,post,pin,qs,email,dep)
        iud(qry1,value1)
        print(value1)
        return '''<script>alert("Successfully added");window.location='/manage_staff'</script>'''
    except   Exception as e:
        return '''<script>alert("Duplicate entry!!!!!!!");window.location='/manage_staff'</script>'''











@app.route('/admin_home')
def admin_home():
    return render_template('Admin home.html')

@app.route('/assign_work_to_staff')
@login_required
def assign_work_to_staff():
    qry="select * from staff"
    res=selectall(qry)
    return render_template('Assign work to staff.html',val=res)

@app.route('/work_assign',methods=['post'])
@login_required
def work_assign():
    sid=request.form['select']
    work=request.form['textfield']
    dis=request.form['textfield2']

    qry="insert into work values(null,%s,%s,%s,curdate(),'pending')"
    val=(sid,work,dis)
    iud(qry,val)
    return '''<script>alert("Assigned work");window.location='/hod_home'</script>'''

@app.route('/hod_home')
def hod_home():
    return render_template('Hod home.html')

@app.route('/manage_course',methods=['post','get'])
@login_required
def manage_course():
    qry="SELECT * FROM course"
    res=selectall(qry)
    return render_template('Manage course.html',value=res)

@app.route('/delete_course')
@login_required
def delete_course():
    id = request.args.get('id')
    qry = "DELETE FROM course WHERE courseid=%s"
    iud(qry, id)
    return '''<script>alert("Successfully deleted");window.location='/manage_course'</script>'''


@app.route('/manage_department')
@login_required
def manage_department():
    qry="select *from department"
    res=selectall(qry)
    return render_template('Manage department.html',value=res)

@app.route('/delete_department')
@login_required
def delete_department():
    id=request.args.get('id')
    qry="DELETE FROM `department` WHERE `did`=%s"
    val=(str(id))
    iud(qry,val)
    return '''<script>alert("Successfully deleted");window.location='/manage_department'</script>'''

@app.route('/manage_HOD',methods=['post','get'])
@login_required
def manage_HOD():
    qry="SELECT `hod`.*,`department`.`department` FROM `hod` JOIN `department` ON`department`.`did`=`hod`.`depid`"
    res=selectall(qry)
    return render_template('Manage HOD.html',value=res)

@app.route('/edit_hod')
@login_required
def edit_hod():
    id=request.args.get('id')
    session['eid']=id
    qry="SELECT * FROM `hod` WHERE `hid`=%s"
    val=(str(id))
    res=selectone(qry,val)
    q="SELECT * FROM `department`"
    r=selectall(q)
    return render_template('edit hod.html',val=res,value=r)

@app.route('/edit_student')
@login_required
def edit_student():
    id=request.args.get('id')
    session['sid']=id
    q1="select *from course"
    res1=selectall(q1)
    qry="SELECT * FROM `student` WHERE `loginid`=%s"
    val=(str(id))
    res=selectone(qry,val)
    q="SELECT * FROM `student`"
    r=selectall(q)
    return render_template('edit student.html',val=res,value=r,val1=res1)


@app.route('/hod_editing',methods=['post'])
@login_required
def hod_editing():
    id=session['eid']
    Fn=request.form['textfield']
    Ln=request.form['textfield3']
    Gen=request.form['radiobutton']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    email=request.form['textfield7']
    quali=request.form.getlist('checkbox')
    qs=str.join(',',quali)
    dep=request.form['select']
    qry="UPDATE `hod` SET `fname`=%s,lname=%s,gender=%s,place=%s,post=%s,pin=%s,email=%s,qualification=%s,depid=%s WHERE `hid`=%s"
    val=(Fn,Ln,Gen,place,post,pin,email,qs,dep,str(id))
    iud(qry,val)
    return '''<script>alert("Successfully updated");window.location='/manage_HOD'</script>'''


@app.route('/delete_hod')
@login_required
def delete_hod():
    id=request.args.get('id')
    q="DELETE FROM  `login`  WHERE `id`=%s"
    v=(str(id))
    iud(q,v)
    qry="DELETE FROM  hod  WHERE lid=%s"
    val=(str(id))
    iud(qry,val)
    return '''<script>alert("Successfully deleted");window.location='/manage_HOD'</script>'''

@app.route('/delete_student')
@login_required
def delete_student():
    id=request.args.get('id')
    q="DELETE FROM  `student`  WHERE `loginid`=%s"
    v=(str(id))
    iud(q,v)
    q1 = "DELETE FROM  `login`  WHERE `id`=%s"
    iud(q1,id)
    return '''<script>alert("Successfully deleted");window.location='/manage_student'</script>'''


@app.route('/hod_adding',methods=['post'])
@login_required
def hod_adding():
    try:
        Fn=request.form['textfield']
        Ln=request.form['textfield3']
        Gen=request.form['radiobutton']
        place=request.form['textfield4']
        post=request.form['textfield5']
        pin=request.form['textfield6']
        email=request.form['textfield7']
        quali=request.form.getlist('checkbox')
        qs=str.join(',',quali)
        dep=request.form['select']
        un=request.form['textfield8']
        pswd=request.form['textfield2']


        qry="insert into login values(null,%s,%s,'hod')"
        value=(un,pswd)
        id=iud(qry,value)
        qry1="insert into hod values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value1=(id,Fn,Ln,Gen,place,post,pin,email,qs,dep)
        iud(qry1,value1)
        return '''<script>alert("Successfully added");window.location='/manage_HOD'</script>'''
    except  Exception as e:
        return '''<script>alert("Duplicate entry!!!!!!!");window.location='/manage_HOD'</script>'''




@app.route('/manage_staff')
@login_required
def manage_staff():
    qry = "SELECT staff.*,department.* FROM department JOIN staff WHERE department.did=staff.depid"
    res = selectall(qry)
    return render_template('Manage staff.html',value=res)

@app.route('/delete_staff')
@login_required
def delete_staff():
    id = request.args.get('id')
    qry = "DELETE FROM staff WHERE sid=%s"
    iud(qry, id)
    qry1="delete from login where id=%s"
    iud(qry1,id)
    return '''<script>alert("Successfully deleted");window.location='/manage_staff'</script>'''

@app.route('/edit_staff')
@login_required
def edit_staff():
    id=request.args.get('id')
    session['eid']=id
    qry="SELECT * FROM `staff` WHERE `sid`=%s"
    val=(str(id))
    res=selectone(qry,val)
    q="SELECT * FROM `department`"
    r=selectall(q)
    return render_template('Edit staff.html',val=res,value=r)

@app.route('/staff_editing',methods=['post'])
@login_required
def staff_editing():
    id=session['eid']
    Fn=request.form['textfield']
    Ln=request.form['textfield2']
    Gen=request.form['radiobutton']
    place=request.form['textfield3']
    post=request.form['textfield4']
    pin=request.form['textfield5']
    email=request.form['textfield6']
    quali=request.form.getlist('checkbox')
    qs=str.join(',',quali)
    dep=request.form['select']
    qry="UPDATE `staff` SET `fname`=%s,lname=%s,gender=%s,place=%s,post=%s,pin=%s,qualification=%s,email=%s,depid=%s WHERE `sid`=%s"
    val=(Fn,Ln,Gen,place,post,pin,qs,email,dep,str(id))
    iud(qry,val)
    return '''<script>alert("Successfully updated");window.location='/manage_staff'</script>'''



@app.route('/manage_student',methods=['post','get'])
@login_required
def manage_student():
    qry = "SELECT `student`.*,`course`.`coursename` FROM student JOIN `course` ON `student`.courseid=`course`.`courseid`"
    res = selectall(qry)

    return render_template('Manage student.html',value=res)

@app.route('/add_student',methods=['post','get'])
@login_required
def add_student():
    qry = "select *from course"
    res = selectall(qry)
    return render_template('Add student.html',val=res)

@app.route('/adding_student',methods=['post','get'])
@login_required
def adding_student():
    try:

        Fn = request.form['textfield']
        Ln = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pin = request.form['textfield5']
        photo=request.files['file']
        fn=secure_filename(photo.filename)
        photo.save(os.path.join('static/student pic',fn))
        cid=request.form['select']
        sem = request.form['select2']
        age = request.form['textfield6']
        gen = request.form['radiobutton']
        email = request.form['textfield7']
        phone = request.form['textfield8']
        uname = request.form['textfield9']
        pwd=request.form['textfield10']
        qry="insert into login values(null,%s,%s,'student')"
        value=(uname,pwd)
        id=iud(qry,value)
        qry1 = "insert into student values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value1 = (id,Fn,Ln,place,post,pin,fn,cid,sem,age,gen,email,phone)
        iud(qry1, value1)
        return '''<script>alert("Successfully added");window.location='/manage_student'</script>'''
    except  Exception as e:
        return '''<script>alert("Duplicate entry!!!!!!!");window.location='/manage_student'</script>'''



@app.route('/editing_student',methods=['post','get'])
@login_required
def editing_student():
    try:
        Fn = request.form['textfield']
        Ln = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pin = request.form['textfield5']
        photo = request.files['file']
        fn = secure_filename(photo.filename)
        photo.save(os.path.join('static/student pic', fn))
        cid=request.form['select']
        sem = request.form['select']
        age = request.form['textfield6']
        gen = request.form['radiobutton']
        email = request.form['textfield7']
        phone = request.form['textfield8']


        qry1 = "update student SET `fname`=%s,`lname`=%s,`place`=%s,`post`=%s,pin=%s,`photo`=%s,`courseid`=%s,`sem`=%s,`age`=%s,`gender`=%s,`email`=%s,`phone`=%s where loginid=%s"
        value1 = (Fn,Ln,place,post,pin,fn,cid,sem,age,gen,email,phone,session['sid'])
        iud(qry1, value1)
        return '''<script>alert("Successfully added");window.location='/manage_student'</script>'''
    except:
        Fn = request.form['textfield']
        Ln = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pin = request.form['textfield5']
        cid = request.form['select']
        sem = request.form['select']
        age = request.form['textfield6']
        gen = request.form['radiobutton']
        email = request.form['textfield7']
        phone = request.form['textfield8']

        qry1 = "update student SET `fname`=%s,`lname`=%s,`place`=%s,`post`=%s,pin=%s,`courseid`=%s,`sem`=%s,`age`=%s,`gender`=%s,`email`=%s,`phone`=%s where loginid=%s"
        value1 = (Fn, Ln, place, post, pin, cid, sem, age, gen, email, phone, session['sid'])
        iud(qry1, value1)
        return '''<script>alert("Successfully added");window.location='/manage_student'</script>'''






@app.route('/reply')
@login_required
def reply():
    return render_template('reply.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/send_complaint')
@login_required
def send_complaint():
    id = request.args.get('id')
    session['cid'] = id
    return render_template('Send complaint.html')

@app.route('/sending_complaints',methods=['post','get'])
@login_required
def sending_complaints():
    complaint=request.form['textfield']
    qry="insert into complaint values(null,%s,%s,curdate(),'pending');"
    val=(session['id'],complaint)
    iud(qry,val)
    return '''<script>alert("Complaint send");window.location='/view_reply'</script>'''


@app.route('/send_feedback')
@login_required
def send_feedback():
    id = request.args.get('id')
    session['userid'] = id
    return render_template('Send feedback.html')

@app.route('/sending_feedback',methods=['post','get'])
@login_required
def sending_feedback():
        feedback = request.form['textfield']
        qry = "insert into feedback values(null,%s,%s,curdate(),'pending')"
        val = (session['id'],feedback)
        iud(qry, val)
        return '''<script>alert("feedback send");window.location='/staff_home'</script>'''


@app.route('/send_reply',methods=['post','get'])
@login_required
def send_reply():
    id=request.args.get('id')
    session['cid']=id
    return render_template('Send reply.html')

@app.route('/send_reply2',methods=['post','get'])
@login_required
def send_reply2():
    reply=request.form['textfield']
    qry="UPDATE complaint SET reply=%s WHERE cid=%s"
    val=(reply,session['cid'])
    iud(qry,val)
    return '''<script>alert("Reply send");window.location='/view_complaint'</script>'''





@app.route('/send_reply3',methods=['post','get'])
@login_required
def send_reply3():
    id=request.args.get('id')
    session['cid']=id
    return render_template('reply.html')

@app.route('/send_reply4',methods=['post','get'])
@login_required
def send_reply4():
    reply=request.form['textfield']
    qry="UPDATE complaint SET reply=%s WHERE cid=%s"
    val=(reply,session['cid'])
    iud(qry,val)
    return '''<script>alert("Reply send");window.location='/view_complaint'</script>'''






@app.route('/staff_home')

def staff_home():
    return render_template('Staff home.html')




@app.route('/update_status',methods=['post','get'])
@login_required
def update_status():
    id=request.args.get('id')
    session['wid']=id
    return render_template('Update status.html')

@app.route('/updating_status',methods=['post','get'])
@login_required
def updating_status():
    status=request.form['textfield']
    qry="UPDATE work SET status=%s WHERE wid=%s"
    val=(status,session['wid'])
    iud(qry,val)
    return '''<script>alert("Status updated");window.location='/view_work'</script>'''




@app.route('/view_complaint',methods=['post','get'])
@login_required
def view_complaint():
    qry = "SELECT staff.fname,staff.lname,complaint.*FROM staff JOIN complaint ON complaint.userid=staff.lid "
    res = selectall(qry)
    return render_template('View complaint.html',val=res)

@app.route('/view_complaint2')
@login_required
def view_complaint2():
    qry = "SELECT staff.fname,staff.lname,complaint.*FROM staff JOIN complaint ON complaint.userid=staff.lid JOIN `login` ON `complaint`.`userid`=`login`.`id` WHERE `login`.`type`='staff' AND `complaint`.`reply`='pending'"
    res = selectall(qry)
    return render_template('View complaint2.html',val=res)

@app.route('/view_feedback')
@login_required
def view_feedback():
    qry = "SELECT staff.fname,staff.lname,feedback.*FROM staff JOIN feedback ON feedback.userid=staff.lid"
    res = selectall(qry)
    return render_template('view feedback.html', value=res)


@app.route('/view_feedback2')
@login_required
def view_feedback2():
    qry = "SELECT staff.fname,staff.lname,feedback.*FROM staff JOIN feedback ON feedback.userid=staff.lid"
    res = selectall(qry)
    return render_template('View feedback2.html',value=res)

@app.route('/view_mask_notification')
@login_required
def view_mask_notification():
    qry = "SELECT student.fname,student.lname,course.coursename,camnotification.image,camnotification.datetime  FROM student JOIN camnotification ON camnotification.sid=student.loginid JOIN course ON course.courseid=student.courseid"
    res = selectall(qry)
    return render_template('View mask notification.html',value=res)

@app.route('/view_mask_notification2')
@login_required
def view_mask_notification2():
    qry = "SELECT student.fname,student.lname,course.coursename,camnotification.image,camnotification.datetime  FROM student JOIN camnotification ON camnotification.sid=student.loginid JOIN course ON course.courseid=student.courseid"
    res = selectall(qry)
    return render_template('View mask notification2.html',value=res)

@app.route('/view_mask_notification3')
@login_required
def view_mask_notification3():
    qry = "SELECT student.fname,student.lname,course.coursename,camnotification.image,camnotification.datetime  FROM student JOIN camnotification ON camnotification.sid=student.loginid JOIN course ON course.courseid=student.courseid"
    res = selectall(qry)
    return render_template('View mask notification3.html',value=res)

@app.route('/view_reply')
@login_required
def view_reply():
    qry="select* from complaint where userid=%s"
    res=selectall2(qry,session['id'])
    return render_template('View reply.html',value=res)

@app.route('/view_work')
@login_required
def view_work():
    qry = "select* from work"
    res = selectall(qry)
    return render_template('View work.html',value=res)

@app.route('/login_code',methods=['post'])
def login_code():
    username=request.form['textfield']
    password=request.form['textfield2']
    query="select *from login where username=%s and password=%s"
    value=(username,password)

    res=selectone(query,value)
    if res is None:
        return'''<script>alert("invalid");window.location='/logout'</script>'''
    else:
        if res[3]=='admin':
            session['id'] = res[0]
            return redirect('/admin_home')
        elif res[3]=='hod':
            session['id'] = res[0]
            return redirect('/hod_home')
        elif res[3]=='staff':
            session['id']=res[0]
            return redirect('/staff_home')

        else:
            return '''<script>alert("invalid");window.location='/logout'</script>'''








































app.run(debug=True)