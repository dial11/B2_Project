from flask import Flask, render_template
import pymysql
import json

app = Flask(__name__)


@app.route('/')
def root():
    print('show_all')
    return render_template('index.html', category_name='all')


@app.route('/category-backend')
def backendLayout():
    print('show_backend')
    return render_template('index.html', category_name='backend')


@app.route('/category-frontend')
def frontendLayout():
    print('front_backend')
    return render_template('index.html', category_name='frontend')


@app.route('/user', methods=['GET'])
def get_users():
    print('get_users')
    db = pymysql.connect(host='localhost', user='root', db='project2b2', password='10041004',
                         charset='utf8')
    curs = db.cursor()

    sql_user = """
        SELECT u.email, u.password, u.name, u.description
        FROM user u
        """

    curs.execute(sql_user)
    rows_user = curs.fetchall()
    print(rows_user)

    json_str = json.dumps(rows_user, indent=4, sort_keys=True, default=str)

    db.commit()
    db.close()
    return json_str, 200


@app.route('/board', methods=['GET'])
def get_boards():
    print('get_boards')
    db = pymysql.connect(host='localhost', user='root', db='project2b2', password='10041004',
                         charset='utf8')
    curs = db.cursor()

    sql_board = """
        SELECT b.title, b.content, b.created_at, u.name, c.name
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        ORDER BY b.id
        """

    curs.execute(sql_board)
    rows_board = curs.fetchall()
    print(rows_board)

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str)

    db.commit()
    db.close()
    return json_str, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
