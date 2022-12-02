from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
app = Flask(__name__)

@app.route('/login')
def home():
    return render_template('login.html')

@app.route('/post')
def home():
    return render_template('post.html')

# @app.route('/user/login', methods=['POST'])
# def save_user():

#     userName = {'name': request.form['name']}

#     userName = request.form['name']

#     sql = 'INSERT INTO user(name) VALUES(%s)'

#     app.database.execute(sql, (userName)).lastrowid #실행한 테이블의 마지막 행 아이디를 가져옴.

#     return jsonify({'msg':'등록성공'})

if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    app.run('0.0.0.0', port=5000, debug=True)