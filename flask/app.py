from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'q1w2e3'
app.config['MYSQL_DB'] = 'memories'

mysql = MySQL(app)

def wait_for_db():
    with app.app_context():
        for i in range(10):
            try:
                mysql.connection.cursor()
                print("MySQL 연결 성공!")
                return
            except:
                print(f"MySQL 대기중... ({i+1}/10)")
                time.sleep(3)

wait_for_db()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (name, password) VALUES (%s, %s)",
                    (data['name'], data['pw']))
        mysql.connection.commit()
        return login()
    except:
        return jsonify({'ok': False, 'msg': '이미 있는 이름이에요'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, name FROM users WHERE name=%s AND password=%s",
                (data['name'], data['pw']))
    user = cur.fetchone()
    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        return jsonify({'ok': True, 'name': user[1]})
    return jsonify({'ok': False, 'msg': '이름 또는 비밀번호가 틀렸어요'})

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'ok': True})

@app.route('/categories')
def categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT cate_id, cate_name FROM category")
    rows = cur.fetchall()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

@app.route('/reviews')
def get_reviews():
    cate_id = request.args.get('cate_id')
    cur = mysql.connection.cursor()
    if cate_id:
        cur.execute("""
            SELECT r.review_id, u.name, r.title, c.cate_name,
                   r.picture, r.link, r.writing, r.rating, r.create_date
            FROM review r
            JOIN users u ON r.user_id = u.user_id
            JOIN category c ON r.cate_id = c.cate_id
            WHERE r.cate_id = %s
            ORDER BY r.create_date DESC
        """, (cate_id,))
    else:
        cur.execute("""
            SELECT r.review_id, u.name, r.title, c.cate_name,
                   r.picture, r.link, r.writing, r.rating, r.create_date
            FROM review r
            JOIN users u ON r.user_id = u.user_id
            JOIN category c ON r.cate_id = c.cate_id
            ORDER BY r.create_date DESC
        """)
    rows = cur.fetchall()
    result = []
    for r in rows:
        result.append({
            'id': r[0], 'user_name': r[1], 'title': r[2],
            'category': r[3], 'picture': r[4], 'link': r[5],
            'writing': r[6], 'rating': float(r[7]),
            'date': str(r[8])
        })
    return jsonify(result)

@app.route('/reviews', methods=['POST'])
def post_review():
    if 'user_id' not in session:
        return jsonify({'ok': False, 'msg': '로그인 필요'})
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO review (user_id, title, cate_id, picture, link, writing, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (session['user_id'], data['title'], data['cate_id'], 
          data.get('picture', ''), data.get('link', ''),
          data['writing'], data['rating']))
    mysql.connection.commit()
    return jsonify({'ok': True})

# 댓글 목록 - user_name 포함
@app.route('/reviews/<int:review_id>/comments')
def get_comments(review_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.id, c.comment, c.create_date, u.name
        FROM comment c
        LEFT JOIN users u ON c.user_id = u.user_id
        WHERE c.review_id = %s
    """, (review_id,))
    rows = cur.fetchall()
    return jsonify([{'id': r[0], 'comment': r[1], 'date': str(r[2]), 'user_name': r[3]} for r in rows])

# 댓글 작성 - user_id 포함
@app.route('/reviews/<int:review_id>/comments', methods=['POST'])
def post_comment(review_id):
    if 'user_id' not in session:
        return jsonify({'ok': False, 'msg': '로그인 필요'})
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO comment (review_id, comment, user_id) VALUES (%s, %s, %s)",
                (review_id, data['comment'], session['user_id']))
    mysql.connection.commit()
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)