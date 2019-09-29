from flask import Flask 
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Mysql configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskdemo'


mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=="GET":
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        
        users = cursor.fetchall()
        allData = []

        for i in range(len(users)):
            id = users[i][0]
            name = users[i][1]
            age = users[i][2]
            dataDict = {
                "id": id,
                "name": name,
                "age": age
            }
            allData.append(dataDict)

        return jsonify(allData)
    else:
        body = request.json
        name = body['name']
        age = body['age']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users VALUES(null, %s, %s)', (str(name), str(age)))
        mysql.connection.commit()
        cursor.close()
        return jsonify({
            'status': 'Data is posted to MySQL!',
            'name': name,
            'age': age
        })

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        users = cursor.fetchall()
        print(users)
        data = []
        for i in range(len(users)):
            id = users[i][0]
            name = users[i][1]
            age = users[i][2]
            dataDict = {
                "id": id,
                "name": name,
                "age": age
            }
            data.append(dataDict)
        return jsonify(data)
        
    # DELETE a data
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'Data '+id+' is deleted on MySQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        print ("inside put method")
        body = request.json
        name = body['name']
        age = body['age']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET name = %s, age = %s WHERE id = %s', (name, age, id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'Data '+id+' is updated on MySQL!'})

if __name__ == "__main__":
    app.run()       