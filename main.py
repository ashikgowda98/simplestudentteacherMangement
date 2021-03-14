from flask import Flask,flash, url_for, redirect, render_template, request
import sqlite3
from flask import Markup
app = Flask(__name__)
app.secret_key = b'secret_key'
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/studentsignup',methods=['GET', 'POST'])
def studentsignup():
    if request.method == 'POST':
        usn = request.form['USN']
        name = request.form['NAME']
        dob = request.form['DOB']
        email = request.form['EMAIL']
        phone = request.form['PHONE']
        address = request.form['ADDRESS']
        db=sqlite3.connect('studentdb.db')
        cur=db.cursor()
        
        sql='''insert into studentinfo(USN,NAME,DOB,EMAIL,PHONE,ADDRESS)values(?,?,?,?,?,?)'''
        query=(usn,name,dob,email,phone,address,)
        cur.execute(sql,query)
        db.commit()
        db=sqlite3.connect('studentdb.db')
        cur=db.cursor()
        
        sql='''insert into details(USN,SEM1,SEM2,SEM3,SEM4,SEM5,SEM6,SEM7,SEM8)values(?,?,?,?,?,?,?,?,?)'''
        query=(usn,0,0,0,0,0,0,0,0,)
        cur.execute(sql,query)
        db.commit()
        flash('You were successfully signed up')
        return render_template('index.html')
    return render_template('studentsignup.html')




@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    error = None
    db=sqlite3.connect('studentdb.db')
    cur=db.cursor()
    if request.method == 'POST':
        x=request.form['USN'] 
        sql = '''SELECT USN FROM studentinfo  WHERE USN = ?'''
        query = (x,)
        cur.execute(sql,query)
        h = cur.fetchall()
       
        if len(h)!=0:
            sql = '''SELECT * FROM studentinfo  WHERE USN = ?'''
            query = (x,)
            cur.execute(sql,query)
            sim = cur.fetchall()
            sql = '''SELECT * FROM details  WHERE USN = ?'''
            query = (x,)
            cur.execute(sql,query)
            simple = cur.fetchall()
            return render_template('studentinfo.html', data = simple,data1 = sim)
        else:
            flash("invalid usn")
            error="invalid usn"
            return render_template('studentlogin.html')
    return render_template('studentlogin.html', error=error)
            
@app.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    error = None
    db=sqlite3.connect('studentdb.db')
    cur=db.cursor()
    if request.method == 'POST':
        x=request.form['TID']
        password=request.form['PASSWORD']
        sql = '''SELECT password FROM teacherinfo  WHERE TID = ?'''
        query = (x,)
        cur.execute(sql,query)
        h = cur.fetchall()
        if len(h)!=0:
            if h[0][0]==password:
                sql = '''SELECT * FROM details '''
                
                cur.execute(sql,)
                simple = cur.fetchall()
                return render_template('teacherenter.html', data = simple)
            else:
                flash("invalid password")
                error="invalid password"
                return render_template('teacherlogin.html')
        else:
            flash('invalid TID')
            return render_template('teacherlogin.html')
    return render_template('teacherlogin.html', error=error)


@app.route('/update/<USN>',methods=['GET', 'POST'])
def update(USN):
    db=sqlite3.connect('studentdb.db')
    cur=db.cursor()
    
    x='%s'%USN
    sql = '''SELECT * FROM details WHERE USN=? '''
    query=(x,)
    cur.execute(sql,query)
    simple=cur.fetchall()
    return render_template('update1.html', data = simple)

@app.route('/update2',methods=['GET','POST']) 
def update2():
    if request.method == 'POST':
        usn=request.form['usn']
        sem1=request.form['sem1']
        sem2=request.form['sem2']
        sem3=request.form['sem3']
        sem4=request.form['sem4']
        sem5=request.form['sem5']
        sem6=request.form['sem6']
        sem7=request.form['sem7']
        sem8=request.form['sem8']
        db=sqlite3.connect('studentdb.db')
        cur=db.cursor()
        sql='''UPDATE  details SET SEM1=?,SEM2=?,SEM3=?,SEM4=?,SEM5=?,SEM6=?,SEM7=?,SEM8=? WHERE USN=?'''
        query=(sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8,usn)
        cur.execute(sql,query,)
        db.commit()
        db=sqlite3.connect('studentdb.db')
        cur=db.cursor()
        sql = '''SELECT * FROM details '''
        cur.execute(sql,)
        simple = cur.fetchall()
        return render_template('teacherenter.html', data = simple)
    return render_template('teacherenter.html')



    
@app.route('/delete/<USN>',methods=['GET', 'POST'])
def delete(USN):
    db=sqlite3.connect('studentdb.db')
    cur=db.cursor()
    
    x='%s'%USN
    sql = '''DELETE FROM details WHERE USN=?'''
    query=(x,)
    cur.execute(sql,query)
    db.commit()
    db=sqlite3.connect('studentdb.db')
    cur=db.cursor()
    sql = '''SELECT * FROM details '''
    cur.execute(sql,)
    simple = cur.fetchall()
    return render_template('teacherenter.html', data = simple)
    
    





    

        
if __name__ == '__main__':

    app.run(host="0.0.0.0")