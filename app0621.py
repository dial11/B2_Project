from flask import Flask, render_template, request, jsonify
import pymysql
# from sqlalchemy import create_engine

db = pymysql.connect(host="gotiger.ipdisk.co.kr", user="project2b2", passwd="project2b2", db="project2b2", charset="utf8")
cur = db.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('useredit.html')

@app.route('/api/user', methods=['GET'])
def get_user():

    sql = "SELECT id, name, email FROM student"
    cur.execute(sql)

    data_list = cur.fetchall()

    user_list = []

    # print([data_list])

    for record in data_list:
        temp = {
            'id': record[0],
            'name': record[1],
            'email': record[2]
        }
        user_list.append(temp)
    # print(user_list)
    db.commit()

    return jsonify({'msg':  user_list})

@app.route('/api/user', methods=['POST'])
def save_user():

    userName = request.form['name']
    userEmail = request.form['email']

    sql = '''INSERT INTO `student` (name, email) VALUES(%s, %s);'''

    cur.execute(sql, (userName, userEmail))
    db.commit()

    return jsonify({'msg': "등록성공!"})

@app.route('/api/user', methods=['DELETE'])
def del_user():

    user_id_receive = request.form['user_id_give']
    # print(del_id_receive)

    sql = '''DELETE FROM `project2b2`.`student` WHERE  `id`=%s;'''

    cur.execute(sql, (user_id_receive))
    db.commit()

    return jsonify({'msg': "삭제성공!"})

@app.route('/api/user', methods=['PATCH'])
def patch_user():

    patchUserName_receive = request.form['patchUserName_give']
    patchUserEmail_receive = request.form['patchUserEmail_give']
    user_id_receive = request.form['user_id_give']

    sql = '''UPDATE `project2b2`.`student` SET name=%s,email=%s WHERE id=%s;'''

    cur.execute(sql, (patchUserName_receive, patchUserEmail_receive, user_id_receive))
    db.commit()

    return jsonify({'msg': "수정성공!"})


if __name__ == '__main__' :
    app.run('0.0.0.0', port=5000, debug=True)