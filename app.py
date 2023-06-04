from flask import Flask, render_template, request, url_for, flash, redirect, Response
from forms import RegistrationForm, LoginForm, gameForm
import sqlite3 as sql
from flask import session
import os
import cv2
import random

# mambers table 생성
"""
# db create & connect
conn=sql.connect('database.db')
print("create & connect database")

# table create
conn.execute(
    '''
    create table members(name text, id text, password text, point INTEGER default 500,
                        PRIMARY KEY("id"))
    '''
)

conn.close()
"""
# score table 생성
'''
conn=sql.connect('database.db')
print("create & connect database")
conn.execute(
    """
    create table score("game_id" INTEGER, "id" text, "result" text, "game_point" INTEGER,
                        PRIMARY KEY("game_id"),
                        FOREIGN KEY("id") REFERENCES members)

    """
    )
print("create table score(game_id INTEGER, id )")


conn.close()
'''

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

@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        user_id=session.get('user_id',None)
        if 'end' in request.args: # 종료하기 버튼 누른 경우
            with sql.connect("database.db") as con:
                print("1")
                cur=con.cursor()
                cur.execute("select game_point from score where game_id=(?)",(session['game_id'],))
                print("2")
                game_point=cur.fetchone()[0]
                cur.execute("update members set point=point+(?) WHERE id=(?)",(game_point-100,session['user_id']))
                con.commit()
                print("갱신 완료")
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
            return render_template('login.html', msg=msg, form=LoginForm())
    
    return render_template('register.html', form=form)

# 가입 회원 목록 확인
@app.route('/list')
def list():
    con=sql.connect("database.db")
    con.row_factory=sql.Row

    cur=con.cursor()
    cur.execute("select * from members")

    rows=cur.fetchall()
    return render_template("list.html",rows=rows)

# 로그인
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
                    user_id=user[1]
                    session['user_id'] = user_id
                    msg="Login 성공"
                else:
                    msg="비밀번호가 일치하지 않습니다."
        except:
            msg="Error"

        finally:
            con.close()
            return render_template('result.html', msg=msg, user_id=user_id)
        
    return render_template('login.html', form=form)

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 게임 화면
@app.route('/game', methods=["GET", "POST"])
def game():
    form=gameForm()
    rsp=["가위", "바위", "보"]
    if request.method == 'GET':
        if 'continue' in request.args: # 계속하기 버튼을 누른 경우
            print("계속하기 버튼 누름")
        else: # 게임 시작 버튼을 누른 경우
            with sql.connect("database.db") as con:
             cur=con.cursor()
             cur.execute("insert INTO score (id, game_point) VALUES (?, ?)",(session['user_id'],100))
             con.commit()

             # cur=con.cursor()
             cur.execute("select game_id FROM score WHERE rowid = last_insert_rowid()")
             game_id = cur.fetchone()[0]  # 게임 ID 값 가져옴. fetchone()은 튜플을 반환
             session['game_id']=game_id
             print("INSERT 성공")
             
        com=random.choice(rsp) # GET 방식일 경우 com 값 랜덤 지정
        session['com'] = com # session에 저장
        return render_template('game.html', com=com, form=form)
    
    elif request.method=='POST':
        try:
            com=session['com'] # session에 저장된 com 값 사용
            hand = form.hand.data
            if com==hand:
                msg="비겼습니다!"
            elif com=="가위":
                if hand=="바위":
                    msg="이겼습니다!"
                else:
                    msg="졌습니다ㅠㅠ"
            elif com=="바위":
                if hand=="가위":
                    msg="졌습니다ㅠㅠ"
                else:
                    msg="이겼습니다!"
            elif com=="보":
                if hand=="가위":
                    msg="이겼습니다!"
                else:
                    msg="졌습니다ㅠㅠ"

        except:
            msg="Error"
        finally:
            with sql.connect("database.db") as con:
                cur=con.cursor()
            if msg=="이겼습니다!":
                cur.execute("update score set game_point=game_point*2 WHERE game_id=(?)",(session['game_id'],))
                con.commit()
                print("게임 point x 2 성공")
            elif msg=="졌습니다ㅠㅠ":
                cur.execute("update score set game_point=0 WHERE game_id=(?)",(session['game_id'],))
                con.commit()
            return render_template('game_result.html', msg=msg) # 게임 결과 화면으로 이동

            
if __name__ == '__main__':
    app.run(debug=True)