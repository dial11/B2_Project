from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql
import json

app = Flask(__name__)


db = pymysql.connect(
    user='project2b2',
    password='project2b2',
    host='182.212.65.173',
    port=3306,
    database='project2b2',
    charset='utf8'
)

curs = db.cursor()


@app.route('/')
def root():
    # print('show_all')
    return render_template('mypage.html', category_name='all')

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('id', None)
    return redirect('/')

@app.route('/category-backend')
def backendLayout():
    # print('show_backend')
    return render_template('index.html', category_name='backend')


@app.route('/category-frontend')
def frontendLayout():
    # print('front_backend')
    return render_template('index.html', category_name='frontend')


@app.route('/user', methods=['GET'])
def get_users():
    # print('get_users')
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )

    curs = db.cursor()

    sql = """
        SELECT u.email, u.password, u.name, u.description
        FROM user u
        """

    curs.execute(sql)
    rows_user = curs.fetchall()
    # print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()
    db.close()

    return json_str, 200


@app.route('/board', defaults={'page': 1})
@app.route('/board/<int:page>')
def get_boards(page):
    # print('get_boards')
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )

    curs = db.cursor()

    perpage = 5
    startat = (page - 1) * perpage

    sql = f"""
        SELECT b.title, b.content, b.created_at, u.name, c.name
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        ORDER BY b.id desc
        LIMIT {perpage}
        OFFSET {startat}
        """

    curs.execute(sql)
    rows_board = curs.fetchall()
    # print(rows_board)

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str)

    db.commit()
    db.close()

    return json_str, 200


# 정지우님

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

    sql = f'select id,password,name,email,description from user where user.id = {userId}'

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
            session['description'] = result[4]
            return jsonify({'msg':'로그인 성공'})

# @app.route('/api/user', methods=['GET'])
# def get_user():

#     sql = "SELECT id, name, email FROM student"
#     cur.execute(sql)

#     data_list = cur.fetchall()

#     user_list = []

#     # print([data_list])

#     for record in data_list:
#         temp = {
#             'id': record[0],
#             'name': record[1],
#             'email': record[2]
#         }
#         user_list.append(temp)
#     # print(user_list)
#     db.commit()

#     return jsonify({'msg':  user_list})

# @app.route('/api/user', methods=['POST'])
# def save_user():

#     userName = request.form['name']
#     userEmail = request.form['email']

#     sql = '''INSERT INTO `student` (name, email) VALUES(%s, %s);'''

#     cur.execute(sql, (userName, userEmail))
#     db.commit()

#     return jsonify({'msg': "등록성공!"})

# @app.route('/api/user', methods=['DELETE'])
# def del_user():

#     user_id_receive = request.form['user_id_give']
#     # print(del_id_receive)

#     sql = '''DELETE FROM `project2b2`.`student` WHERE  `id`=%s;'''

#     cur.execute(sql, (user_id_receive))
#     db.commit()

#     return jsonify({'msg': "삭제성공!"})

# @app.route('/api/user', methods=['PATCH'])
# def patch_user():

#     patchUserName_receive = request.form['patchUserName_give']
#     patchUserEmail_receive = request.form['patchUserEmail_give']
#     user_id_receive = request.form['user_id_give']

#     sql = '''UPDATE `project2b2`.`student` SET name=%s,email=%s WHERE id=%s;'''

#     cur.execute(sql, (patchUserName_receive, patchUserEmail_receive, user_id_receive))
#     db.commit()

#     return jsonify({'msg': "수정성공!"})


# 마이페이지에서 로그인한 유저 게시글 불러오기
@app.route('/user/post', methods=['GET'])
def get_user_post():
    # print('get_users')

    sql = """SELECT u.email, u.password, u.name, u.description FROM user u"""

    curs.execute(sql)
    rows_user = curs.fetchall()
    # print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()
    db.close()

    return json_str, 200



if __name__ == '__main__' :
    app.run('0.0.0.0', port=5000, debug=True)