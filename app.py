from flask import Flask, render_template, request, url_for, flash, redirect, Response
from forms import RegistrationForm, LoginForm
import sqlite3 as sql
from flask import session
import os
import cv2


"""
# db create & connect
conn=sql.connect('database.db')
print("create & connect database")

# table create
conn.execute(
    '''
    create table members(name text, id text, password text)
    '''
)
print("create table")

conn.close()
"""

app = Flask(__name__)
# app.config["SECRET_KEY"] = '123654'
app.config["SECRET_KEY"] = os.urandom(24)
print("secretKey",app.config["SECRET_KEY"])

def generate_frames():
    camera=cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()

        if not success:
            break
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 스트리밍

    camera.release()

@app.route('/')
def main():
    user_id=session.get('user_id',None)
    return render_template('main.html',user_id=user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        try:
            name = form.name.data
            id = form.id.data
            password = form.password.data
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO members (name, id, password) VALUES (?, ?, ?)", (name, id, password))
                con.commit()
                msg = "Success"
        except:
            con.rollback()
            msg = "Error"
        
        finally:
            con.close()
            return render_template('result.html', msg=msg)
    
    return render_template('register.html', form=form)

@app.route('/list')
def list():
    con=sql.connect("database.db")
    con.row_factory=sql.Row

    cur=con.cursor()
    cur.execute("select * from members")

    rows=cur.fetchall()
    return render_template("list.html",rows=rows)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method=='POST':
        try:
            id = form.id.data
            password = form.password.data
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM members WHERE Id=? AND Password=?", (id, password))
                user = cur.fetchone()
                if user:
                    session['user_id'] = user[1]
                    msg="Login 성공"
                else:
                    msg="비밀번호가 일치하지 않습니다."
        except:
            msg="Error"

        finally:
            con.close()
            return render_template('result.html', msg=msg)
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)