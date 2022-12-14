from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import bcrypt
import pymysql
import json
import flash
import os

UPLOAD_FOLDER = 'static/image/post'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = '1221'


@app.route('/')
def show_main():
    return render_template('index.html', component_name='main')


@app.route('/category')
def show_by_category():
    return render_template('index.html', component_name='category')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/category-list', methods=['GET'])
def get_category_list():
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
    rows_category = curs.fetchall()

    json_str = json.dumps(rows_category, indent=4, sort_keys=True, default=str)

    db.commit()

    return json_str, 200


@app.route('/user', methods=['GET'])
def get_users():
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
        SELECT u.id, u.email, u.password, u.name, u.image, u.description
        FROM user u
        """

    curs.execute(sql)
    rows_user = curs.fetchall()

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
        sql = f"""
            SELECT b.id, b.title, b.content, b.created_at, b.updated_at, u.name, u.image, c.name_en, u.id
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
        sql = f"""
            SELECT b.id, b.title, b.content, b.created_at, b.updated_at, u.name, u.image, c.name_en, u.id
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

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str)

    curs.execute('SELECT COUNT(*) FROM board')
    total_num = curs.fetchall()

    db.commit()

    return json_str, 200


# ----------------??????????????? ?????? ??????
# ?????????/???????????????????????? ??????---------------------------
@app.route('/login')
def login():
    return render_template('login.html')


# ????????????????????? ??????
@app.route('/post')
def post():
    return render_template('post.html')


# ????????????
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
                return jsonify({'msg': '????????? ????????? ????????????.'})

        else:
            if list_result[i][0] == userId:
                return jsonify({'msg': '????????? ???????????? ????????????.'})
            elif list_result[i][1] == email:
                return jsonify({'msg': '????????? ???????????? ????????????.'})
            elif list_result[i][2] == userName:
                return jsonify({'msg': '????????? ???????????? ????????????.'})

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
    # ????????? ??????????????? ????????? ????????? ??????
    byte_input = password.encode('UTF-8')
    hash = bcrypt.hashpw(byte_input, bcrypt.gensalt()).hex()
    userName = request.form['name']
    email = request.form['email']

    sql = f'INSERT INTO `user` (id, password, name, email) VALUES("{userId}", "{hash}", "{userName}", "{email}");'

    curs.execute(sql)  # ????????????????????? ???????????? ??????
    db.commit()  # ??????,??????,????????????, ??????????????? ????????????????????? ???????????????
    db.close()

    return jsonify({'msg': '?????? ?????? ??????'})


# ?????????
@app.route('/user/login', methods=['POST'])
def user_login():
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

    # ????????? ??????????????? ????????? ????????? ??????
    byte_input = password.encode('UTF-8')

    sql = f'select id,password,name,email,image,description from user where user.id = "{userId}"'

    curs.execute(sql)
    result = curs.fetchone()
    list_result = list(result)
    # ?????? ????????? ?????? ????????? ?????? hex?????? ???????????? ??????
    origin_pw = bytes.fromhex(list_result[1])
    pw_check = bcrypt.checkpw(byte_input, origin_pw)

    db.commit()  # ??????,??????,????????????, ??????????????? ????????????????????? ???????????????
    db.close()

    if result is None:
        return jsonify({'msg': '????????? ????????????.'})

    else:
        if not pw_check:
            return jsonify({'msg': '??????????????? ???????????? ????????????.'})
        else:
            session['id'] = result[0]
            session['name'] = result[2]
            session['email'] = result[3]
            session['image'] = result[4]
            session['description'] = result[5]
            return jsonify({'msg': '????????? ??????'})


# ????????? ????????????
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

    sql1 = f'INSERT INTO project2b2.board(title,content,created_at,category_id,user_id) VALUES (%s, %s, NOW(), %s, %s)'

    # ????????????????????? ???????????? ??????
    curs.execute(sql1, (postTitle, postContent, selectPost, userId))

    db.commit()  # ??????,??????,????????????, ??????????????? ????????????????????? ???????????????
    db.close()

    return redirect('/')


# ?????????????????? ???????????????
@app.route('/post/image', methods=['POST'])
def post_image():
    f = request.files['file']
    f.save('static/image/post/' + f.filename)
    url = "static/image/post/" + f.filename
    return jsonify({'url': url})


# ???????????????-----------------------------------------------------
@app.route('/find/id', methods=['POST'])
def findId():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    email = request.form['email']

    sql_check = f'select id from `user` where email = "{email}" '

    curs.execute(sql_check)
    result = curs.fetchone()

    db.commit()
    db.close()

    if result is None:
        return jsonify({'msg': '????????? ????????????.'})

    return jsonify({'msg': result[0]})


# ????????????-----------------------------------------------------
@app.route('/delete/user', methods=['POST'])
def deleteUser():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    idf = request.form['idf']
    pwf = request.form['pwf']
    byte_input = pwf.encode('UTF-8')

    sql_check = f'select password from `user` where id = "{idf}" '

    curs.execute(sql_check)
    result = curs.fetchone()
    if result is None:
        return jsonify({'msg': '????????? ????????????.'})

    origin_pw = bytes.fromhex(result[0])
    pw_check = bcrypt.checkpw(byte_input, origin_pw)
    db.commit()
    db.close()

    if pw_check is None:
        return jsonify({'msg': '????????? ????????????.'})

    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    idf = request.form['idf']
    pwf = request.form['pwf']

    sql_check = f'delete from `user` where id = "{idf}" '

    curs.execute(sql_check)
    db.commit()
    db.close()

    return jsonify({'msg': '??????????????? ???????????????.'})


# ----------------??????????????? ?????? ??????


# ----------------???????????? ?????? ??????
@app.route('/useredit')
def useredit():
    return render_template('useredit.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


# ????????????????????? ???????????? ?????? ????????? ????????????
@app.route('/user/post', methods=['GET'])
def get_user_post():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = session['id']

    sql = '''SELECT  `title`, `content`, `created_at`, `id` FROM board WHERE user_id = %s;'''
    curs.execute(sql, (userId))
    rows_user = curs.fetchall()

    print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)
    return json_str, 200


# ??????????????? ??????(?????? ?????? ????????????)
@app.route('/user/edit', methods=['GET'])
def edit_get_user():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = session['id']

    sql = '''SELECT `password`, `name`, `email`, `description`, `image` FROM user WHERE id = %s;'''

    curs.execute(sql, (userId))
    rows_user = curs.fetchone()

    return jsonify({'msg': rows_user})


# ??????????????? ????????? ??????
@app.route('/user/edit', methods=['POST'])
def user_img_post():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor(pymysql.cursors.DictCursor)

    # ?????? ????????? ??????
    file = request.files["file_give"]
    userId = session['id']

    if not os.path.isdir("static/image/user"):
        os.makedirs('static/image/user')  # upload/image ?????? ?????? ?????? ????????????
    if file:
        # ?????? ???????????? jpg??? ???????????? ???????????? ?????? ???????????? ?????? ????????? ????????? split??? ??????
        extension = file.filename.split('.')[-1]
        today = datetime.now()
        mtime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{userId}-{mtime}.{extension}'
        save_to = f'static/image/user/{filename}'
        file.save(save_to)

        sql = f'UPDATE `project2b2`.`user` SET image="{filename}" WHERE id="{userId}";'

        curs.execute(sql)
        session['image'] = filename
    db.commit()
    db.close()

    return jsonify({'msg': '????????? ???????????????.'})


# ??????????????? ????????? ??????
@app.route('/user/edit', methods=['DELETE'])
def user_img_del():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = session['id']

    sql = f'UPDATE `project2b2`.`user` SET image="baseprofile.png" WHERE id="{userId}";'

    curs.execute(sql)
    session['image'] = "baseprofile.png"
    db.commit()
    db.close()

    return jsonify({'msg': '????????? ???????????? ?????????????????????.'})


# ??????????????? ??????(?????? ?????? ????????????)
@app.route('/user/edit', methods=['PATCH'])
def edit_user_post():
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    eName_receive = request.form['eName_give']
    eEmail_receive = request.form['eEmail_give']
    eDesc_receive = request.form['eDesc_give']
    ckpw_receive = request.form['ckpw_give']
    byte_input = ckpw_receive.encode('UTF-8')
    userId = session['id']

    sql = f'SELECT `password` FROM user WHERE id = "{userId}";'

    curs.execute(sql)
    pw = curs.fetchone()
    pw = list(pw)

    origin_pw = bytes.fromhex(pw[0])
    pw_check = bcrypt.checkpw(byte_input, origin_pw)

    db.close()

    if '@' not in eEmail_receive:
        return jsonify({'msg': '????????? ????????? ????????????.'})
    elif (not pw_check):
        return jsonify({'msg': '??????????????? ?????? ????????? ???????????? ???????????????.'})
    else:
        db = pymysql.connect(
            user='project2b2',
            password='project2b2',
            host='182.212.65.173',
            port=3306,
            database='project2b2',
            charset='utf8'
        )
        curs = db.cursor()

        sql = f'UPDATE `project2b2`.`user` SET name="{eName_receive}",email="{eEmail_receive}",description="{eDesc_receive}" WHERE id="{userId}";'

        session['name'] = eName_receive
        session['email'] = eEmail_receive
        session['description'] = eDesc_receive

        curs.execute(sql)
        db.commit()
        db.close()

        return jsonify({'msg': '????????? ?????????????????????.'})


# ----------------???????????? ?????? ??????


# ----------------??????????????? ?????? ??????
@app.route('/<int:board_id>')
def boardout(board_id):
    return render_template('board.html', board_id=board_id)


@app.route('/<int:board_id>/data')
def getBoard(board_id):
    db = pymysql.connect(host='182.212.65.173', user='project2b2',
                         db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()

    sql_board = f"""
        SELECT b.title, b.content, b.created_at, u.name, c.name, b.id, b.updated_at, u.image
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        
        WHERE b.id = '{board_id}'
        """

    curs.execute(sql_board)
    rows_board = list(curs.fetchall())

    try:
        rows_board.append(session["name"])
    except:

        json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str, )
    
    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str, )

    db.commit()
    db.close()
    return json_str, 200


@app.route('/board/delete', methods=['DELETE'])
def del_board():
    db = pymysql.connect(host='182.212.65.173', user='project2b2',
                         db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()
    board_id = request.form['board_id_give']
    sql_board = f"""
        DELETE FROM board
        WHERE id = 
        """ + str(board_id) + """
        """

    curs.execute(sql_board)

    db.commit()
    db.close()

    return jsonify({'result': 'success', 'msg': '?????? ??????!'})


@app.route('/boardedit/<int:board_id>')
def editBoards(board_id):
    return render_template('boardedit.html', board_id=board_id)


@app.route('/boardedit/<int:board_id>/re', methods=["GET"])
def editBoard(board_id):
    db = pymysql.connect(host='182.212.65.173', user='project2b2',
                         db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()

    sql_board = f"""
        SELECT b.title, b.content, b.id
        FROM board b
        
        WHERE b.id = '{board_id}'
        """

    curs.execute(sql_board)
    rows_board = curs.fetchall()

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str, )

    db.commit()
    db.close()
    return json_str, 200


@app.route('/boardedit/<int:board_id>/post', methods=['PATCH'])
def postBoard(board_id):
    db = pymysql.connect(host='182.212.65.173', user='project2b2',
                         db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()

    selectPost = request.form['category_id']
    postTitle = request.form['title']
    postContent = request.form['content']
    # userId = session['id']

    sql1 = f"""UPDATE board b
            SET title = %s , content = %s , category_id = %s , updated_at = NOW() 
            
            WHERE b.id = '{board_id}' """

    curs.execute(sql1, (postTitle, postContent, selectPost))

    db.commit()
    db.close()

    return jsonify({'result': 'success', 'msg': '?????? ??????!'})


# ----------------??????????????? ?????? ??????

@app.route('/userpage')
def userpage():
    return render_template('userpage.html')

@app.route('/userpage/<string:id>')
def showUserpage(id):
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = id

    sql = '''
            SELECT u.name, u.email, u.description, u.image
            FROM user u
            WHERE id = %s;
        '''

    curs.execute(sql, (userId))
    rows_user = curs.fetchall()

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()

    return json_str, 200

@app.route('/userpage/post/<string:id>', methods=['GET'])
def userpage_post(id):
    db = pymysql.connect(
        user='project2b2',
        password='project2b2',
        host='182.212.65.173',
        port=3306,
        database='project2b2',
        charset='utf8'
    )
    curs = db.cursor()

    userId = id

    sql = '''
    SELECT  b.title, b.content, b.created_at, b.id
    FROM board b
    INNER JOIN `user` u
    ON b.user_id = u.id
    WHERE u.id = %s;'''

    curs.execute(sql, (userId))
    rows_user = curs.fetchall()

    print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)
    return json_str, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
