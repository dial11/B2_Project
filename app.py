
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
app = Flask(__name__)

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

    sql = 'INSERT INTO project2b2.user(id, email, password, name) VALUES(%s, %s, %s, %s)'

    app.database.execute(sql, (userId, email, password, userName)).lastrowid #실행한 테이블의 마지막 행 아이디를 가져옴.

    return jsonify({'msg':'회원 가입 성공'})


# 로그인
# @app.route('/user/logn', methods=['POST'])
# def user_login():
#     userId = request.form['id']
#     password = request.form['password']

#     sql = 'INSERT INTO user(id, password) VALUES(%s, %s)'

#     app.database.execute(sql, (userId, password)).lastrowid #실행한 테이블의 마지막 행 아이디를 가져옴.

#     return jsonify({'msg':'로그인 성공'})






if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    app.run('0.0.0.0', port=5000, debug=True)