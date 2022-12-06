from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql
import json

app = Flask(__name__)


db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
cur = db.cursor()




@app.route('/board/<int:board_id>')
def getBoard(board_id):

    db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()

    sql_board = f"""
        SELECT b.title, b.content, b.created_at, u.name, c.name, b.id, b.updated_at
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        ORDER BY b.id
        WHERE b.id = '{board_id}'
        """

    curs.execute(sql_board)
    rows_board = curs.fetchone()
    print(rows_board)

    json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str, )

    db.commit()
    db.close()
    return json_str, 200




@app.route('/board/delete', methods=['DELETE'])
def del_board():

    db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()
    board_id = request.form['board_id_give']
    bid = int(board_id)
    sql_board = f"""
        DELETE FROM board
        WHERE id = 
        """+ str(bid) +"""
        """

    curs.execute(sql_board)

    db.commit()
    db.close()
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


@app.route('/boardedit/<int:id>', methods=["GET"])
def edit_board():
    
        db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
        curs = db.cursor()
        board_id = request.form['board_id_give']
        bid = int(board_id)
        sql_board = f"""
        SELECT b.title, b.content, b.created_at, u.name, c.name, b.id, b.updated_at
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        ORDER BY b.id
        WHERE id =  """+ str(bid) +"""
        """

        curs.execute(sql_board)
        rows_board = curs.fetchone()
    

        json_str = json.dumps(rows_board, indent=4, sort_keys=True, default=str, )

        db.commit()
        db.close()
        return json_str, 200 

@app.route('/boardedit', methods=['POST'])
def postBoard():
        db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
        curs = db.cursor()
        board_id = request.form['board_id_give']
        bid = int(board_id)
        selectPost = request.form['category_id']
        postTitle = request.form['title']
        postContent = request.form['content']
        userId = session['id']
        

        sql1 = f"""UPDATE board SET (title,content,category_id,user_id) = VALUES({postTitle},{postContent},{selectPost},{userId}) 
            WHERE id =  """+ str(bid) +""" """

        
        
        curs.execute(sql1)
    
        db.commit() 

        return jsonify({'msg':'POST 성공'})


    

# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)