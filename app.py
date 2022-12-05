
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy import create_engine, text
import pymysql

app = Flask(__name__)

app.secret_key = '1221'

db = pymysql.connect (
    # 데이터베이스에 접속할 사용자 아이디
    user = 'project2b2',
    # 사용자 비밀번호
    password = 'project2b2',
    # 접속할 데이터베이스의 주소 (같은 컴퓨터에 있는 데이터베이스에 접속하기 때문에 localhost)
    host = '182.212.65.173',
    # 관계형 데이터베이스는 주로 3306 포트를 통해 연결됨
    port = 3306,
    # 실제 사용할 데이터베이스 이름
    database = 'project2b2',
    # 해석
    charset = 'utf8'
)

curs = db.cursor()


@app.route('/')
def root():
    return render_template('index.html')

# 로그인/회원가입페이지로 이동
@app.route('/login')
def login():
    return render_template('login.html')


# 글작성페이지로 이동
@app.route('/post')
def post():
    return render_template('post.html')

# 회원가입
@app.route('/user/register', methods=['POST'])
def save_user():
    userId = request.form['id']
    password = request.form['password']
    userName = request.form['name']
    email = request.form['email']


    sql = f'INSERT INTO project2b2.user(id, email, password, name) VALUES({userId}, {email}, {password}, {userName})'

    curs.execute(sql) # 데이터베이스에 넣어주기 위함
    db.commit() #삽입,삭제,수정할때, 최종적으로 데이터베이스를 만져줄때만

    return jsonify({'msg':'회원 가입 성공'})


# 로그인
@app.route('/user/login', methods=['POST'])
def user_login():
    userId = request.form['id']
    password = request.form['password']
    # userName = request.form['name']

    sql = f'select id,password,name,email from user where user.id = {userId}'

    curs.execute(sql)
    result = curs.fetchone()
    # print(type(result), type(password))
    # return result is None

    if result is None:
        # print('none')
        return jsonify({'msg':'회원이 아닙니다.'})

    else:
        if result[1] != password:
            # print('password')
            return jsonify({'msg':'비밀번호가 일치하지 않습니다.'})

        else:
            # sql = f'select id,name,email from user where user.id = {userId}' 
            # #나중수정
            print(result)
            session['id'] = userId
            session['name'] = result[2]
            session['email'] = result[3]
            return jsonify({'msg':'로그인 성공'})
        
   



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)