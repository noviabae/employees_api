from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Connection to MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'company'
mysql = MySQL(app)

@app.route('/')
def main():
    return 'Restful API with Flask and MySQL'

@app.route('/employee')
def employee():
    return jsonify({'name': 'Novia Syabaniyah',
                    'address': 'Kalideres, West Jakarta',
                    'position': 'Junior Developer',
                    'division': 'IT',
                    'salary': 5000000})

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM employees")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close() 
        return jsonify(data)
    
    elif request.method == 'POST':
        name = request.json['name']
        address = request.json['address']
        position = request.json['position']
        division = request.json['division']  
        salary = request.json['salary']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO EMPLOYEES (name, address, position, division, salary) VALUES (%s, %s, %s, %s, %s)"  # Sesuaikan dengan jumlah kolom yang Anda masukkan
        val = (name, address, position, division, salary)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'your data added successfully'})
      

@app.route('/detailemployee')
def detailemployee():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM EMPLOYEES WHERE id=%s"
        val = (request.args['id'])
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()  

        return jsonify(data)

@app.route('/deleteemployee', methods=['DELETE'])
def deleteemployee():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        employee_id = request.args['id']
        sql = "DELETE FROM EMPLOYEES WHERE id=%s"
        val = (employee_id,)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Employee deleted successfully'})
    else:
        return jsonify({'error': 'Please provide an employee ID to delete'})


@app.route('/updateemployee', methods=['PUT'])
def updateemployee():
    if 'id' in request.args:
        data= request.get_json()

        cursor= mysql.connection.cursor()
        sql= "UPDATE employees set name=%s, address=%s, position=%s, division=%s, salary=%s WHERE id=%s"
        val= (data['name'], data['address'], data['position'], data['division'], data['salary'], request.args['id'])
        cursor.execute(sql,val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'data updated successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55, debug=True)

listA = [2, 3, 4]
listB = [i * i for i in listA]
print(listB)
