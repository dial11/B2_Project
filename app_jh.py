from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql
import json

app = Flask(__name__)


db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
cur = db.cursor()




@app.route('/board/<int:board_id>')
def boardout(board_id):
    print(board_id)
    return render_template('board.html', board_id= board_id)


@app.route('/board/<int:board_id>/data')
def getBoard(board_id):
    
    db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
    curs = db.cursor()

    sql_board = f"""
        SELECT b.title, b.content, b.created_at, u.name, c.name, b.id, b.updated_at, b.data
        FROM board b
        INNER JOIN `user` u
        ON b.user_id = u.id
        INNER JOIN category c
        ON b.category_id = c.id
        
        WHERE b.id = '{board_id}'
        """

    curs.execute(sql_board)
    rows_board = list(curs.fetchall())
    rows_board.append(session["name"])
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
    sql_board = f"""
        DELETE FROM board
        WHERE id = 
        """+ str(board_id) +"""
        """

    curs.execute(sql_board)

    db.commit()
    db.close()
    
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


@app.route('/boardedit/<int:board_id>')
def editBoards(board_id):
    print(board_id)
    return render_template('boardedit.html', board_id= board_id)

@app.route('/boardedit/<int:board_id>/re', methods=["GET"])
def editBoard(board_id):
        db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
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
        db = pymysql.connect(host='182.212.65.173', user='project2b2', db='project2b2', password='project2b2', charset='utf8')
        curs = db.cursor()
        
        selectPost = request.form['category_id']
        postTitle = request.form['title']
        postContent = request.form['content']
        # userId = session['id']
        

        sql1 = f"""UPDATE board b
            SET title = %s , content = %s , category_id = %s , updated_at = NOW() 
             
            WHERE b.id = '{board_id}' """

        
        
        curs.execute(sql1,(postTitle,postContent,selectPost))
    
        
        db.commit() 

        return jsonify({'result': 'success', 'msg': '수정 완료!'})


    

# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)