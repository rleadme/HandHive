from flask import Flask, render_template, request, url_for, flash, redirect, Response
from forms import RegistrationForm, LoginForm, gameForm
import sqlite3 as sql
from flask import session
import os
import cv2
import random
from img_single import image_judge



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


@app.route('/', methods=['GET'])
def home():
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

    return render_template('home.html',user_id=user_id)


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
            print(msg)
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
            return render_template('home.html', user_id=user_id)
        
    return render_template('login.html', form=form)

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/game', methods=["GET", "POST"])
def game():
    form=gameForm()
    
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
             
        return render_template('upload.html')
    
    elif request.method=='POST':
        try:
            rsp=["가위", "바위", "보"]
            com=random.choice(rsp) # com 값 랜덤 지정
            f=request.files['file']
            image_data=f.read()
            hand = image_judge(image_data,'knn_model.xml')
            print(hand)
            if com==hand:
                msg="draw"
            elif com=="가위":
                if hand=="바위":
                    msg="win"
                else:
                    msg="lose"
            elif com=="바위":
                if hand=="가위":
                    msg="lose"
                else:
                    msg="win"
            elif com=="보":
                if hand=="가위":
                    msg="win"
                else:
                    msg="lose"
        except:
            msg="Error"
        finally:
            with sql.connect("database.db") as con:
                cur=con.cursor()
            if msg=="win":
                cur.execute("update score set game_point=game_point*2 WHERE game_id=(?)",(session['game_id'],))
                con.commit()
                print("게임 point x 2 성공")
            elif msg=="lose":
                user_id=session.get('user_id',None)
                cur.execute("update score set game_point=0 WHERE game_id=(?)",(session['game_id'],))
                con.commit()
            return render_template('game_result.html', msg=msg) # 게임 결과 화면으로 이동


@app.route('/upload')
def load_file():
    return render_template('upload.html')

# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f=request.files['file']
#         image_data=f.read() 
#         # f.save(f.filename)
#         print(image_judge(image_data,'knn_model.xml'))
#         return 'file uploaded successfully'
            
if __name__ == '__main__':
    app.run(debug=True)