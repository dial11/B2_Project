from flask import Flask, render_template, request, jsonify
import pymysql

db = pymysql.connect(host="182.212.65.173", user="project2b2", passwd="project2b2", db="project2b2", charset="utf8")
cur = db.cursor()

sql = "SELECT * from category"
cur.execute(sql)

data_list = cur.fetchone()
data_list2 = cur.fetchall()

print(data_list)
print(data_list[0])
print(data_list[1])

print('--------------')

print(data_list2)
print(data_list2[0])
print(data_list2[0][0])
print(data_list2[0][1])


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('useredit.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)