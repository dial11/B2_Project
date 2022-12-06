from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
# from sqlalchemy import create_engine, text
import pymysql, os, flash
import json

UPLOAD_FOLDER = 'static/image/post'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# 준기님코드일부합침----------------------------------------------------------------
@app.route('/')
def show_main():
    print('show_main')
    return render_template('index.html', component_name='main')


@app.route('/category')
def show_by_category():
    print('show_category')
    return render_template('index.html', component_name='category')


@app.route('/mypage')
def show_mypage():
    return render_template('index.html', component_name='mypage')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    return redirect('/')


@app.route('/category-list', methods=['GET'])
def get_category_list():
    print('get_categories')
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
        SELECT c.name, c.name_en
        FROM category c
        """

    curs.execute(sql)
    rows_user = curs.fetchall()
    print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()


    return json_str, 200


@app.route('/user', methods=['GET'])
def get_users():
    print('get_users')
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
    print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()

    return json_str, 200


@app.route('/board', defaults={'category': 'all', 'page': 1})
@app.route('/board/<string:category>/<int:page>')
def get_boards(category, page):
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

    if category == 'all':
        print('get_all_boards')
        sql = f"""
            SELECT b.title, b.content, b.created_at, u.name, c.name_en
            FROM board b
            INNER JOIN `user` u
            ON b.user_id = u.id
            INNER JOIN category c
            ON b.category_id = c.id
            ORDER BY b.id desc
            LIMIT {perpage}
            OFFSET {startat}
            """
    else:
        print(f'get_{category}_boards')
        sql = f"""
            SELECT b.title, b.content, b.created_at, u.name, c.name_en
            FROM board b
            INNER JOIN `user` u
            ON b.user_id = u.id
            INNER JOIN category c
            ON b.category_id = c.id
            WHERE c.name_en = '{category}'
            ORDER BY b.id desc
            LIMIT {perpage}
            OFFSET {startat}
            """

    curs.execute(sql)
    rows_board = curs.fetchall()
    print(rows_board)

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str)

    db.commit()

    return json_str, 200


# 로그인/회원가입페이지로 이동----------------------------------------------------------------
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
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = request.form['id']
    password = request.form['password']
    userName = request.form['name']
    email = request.form['email']

    sql_check = f'select id,email,name from `user`'
    
    curs.execute(sql_check)
    result = curs.fetchall()
    db.close() 

    list_result = list(result)

    for i in range(len(list_result)):
        if list_result[i][1] != email:
            if '@' not in email:
                return jsonify({'msg':'이메일 형식이 아닙니다.'})

        else:
            if list_result[i][0] == userId:
                return jsonify({'msg':'동일한 아이디가 있습니다.'})
            elif list_result[i][1] == email:
                return jsonify({'msg':'동일한 이메일이 있습니다.'})
            elif list_result[i][2] == userName:
                return jsonify({'msg':'동일한 닉네임이 있습니다.'})


    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = request.form['id']
    password = request.form['password']
    userName = request.form['name']
    email = request.form['email']

    print(userId,password,userName,email)
    sql = f'INSERT INTO `user` (id, password, name, email) VALUES("{userId}", "{password}", "{userName}", "{email}");'
    
    curs.execute(sql) # 데이터베이스에 넣어주기 위함
    db.commit() #삽입,삭제,수정할때, 최종적으로 데이터베이스를 만져줄때만
    db.close()

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
            session['id'] = result[0]
            session['name'] = result[2]
            session['email'] = result[3]
            return jsonify({'msg':'로그인 성공'})

# 게시글 등록하기
@app.route('/write', methods=['POST'])
def post_board():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    selectPost = request.form['category-id']
    postTitle = request.form['post-title']
    postContent = request.form['post-content']
    userId = session['id']
    # postFile = request.form['data']
    # userName = request.form['name']
    # print(selectPost, postTitle, postContent, userId)

    sql1 = f'INSERT INTO project2b2.board(title,content,created_at,category_id,user_id) VALUES (%s, %s, NOW(), %s, %s)'
    # sql2 = f'INSERT INTO project2b2.board(data) VALUES(LOAD_FILE("{postFile}"))'
    
    curs.execute(sql1,(postTitle,postContent,selectPost,userId)) # 데이터베이스에 넣어주기 위함
    # curs.execute(sql2)
    db.commit() #삽입,삭제,수정할때, 최종적으로 데이터베이스를 만져줄때만
    db.close()

    return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)