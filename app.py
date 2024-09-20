from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_conn():
    connection = sqlite3.connect('your_database.db')
    return connection


@app.route('/fetch', methods=['GET'])
def fetch():
    # URL - http://127.0.0.1:3002/fetch

    connection = get_conn()
    cur = connection.cursor()
    contacts = cur.execute('SELECT * FROM contact')
    select_data = contacts.fetchall()
    print('select_data: ', select_data)
    connection.close()

    # formating
    results = []
    for single_contact in select_data:
        dict_result = {
            'name': single_contact[0],
            'phone_num': single_contact[1],
        }
        results.append(dict_result)

    return jsonify(results)


@app.route('/insert', methods=['POST'])
def add_new():
    # URL - http://127.0.0.1:3002/insert
    data = request.get_json()
    print('Request Body Data: ', data)
    name = data['name']
    phone_num = data['phone_num']

    connection = get_conn()
    cur = connection.cursor()
    sql_query = f'INSERT INTO contact(name, phone_num) VALUEs ("{name}", "{phone_num}")'
    print('sql_query: ', sql_query)
    cur.execute(sql_query)
    connection.commit()
    connection.close()

    return jsonify({
        'message': 'Data is inserted successfully.'
    })


@app.route('/update', methods=['PUT'])
def update():
    # URL - http://127.0.0.1:3002/update
    data = request.get_json()
    param_phone_num = request.args.get('phone_num')
    print('Request Body Data: ', data)
    print('param_phone_num: ', param_phone_num)
    name = data['name']

    connection = get_conn()
    cur = connection.cursor()
    sql_query = f'UPDATE contact set name = "{name}" where phone_num = "{param_phone_num}"'
    print('sql_query: ', sql_query)
    cur.execute(sql_query)
    connection.commit()
    connection.close()

    return jsonify({
        'message': 'Data is updated successfully.'
    })


@app.route('/delete', methods=['DELETE'])
def delete():
    # URL - http://127.0.0.1:3002/delete
    param_phone_num = request.args.get('phone_num')
    print('param_phone_num: ', param_phone_num)

    connection = get_conn()
    cur = connection.cursor()
    sql_query = f'DELETE FROM contact where phone_num = "{param_phone_num}"'
    print('sql_query: ', sql_query)
    cur.execute(sql_query)
    connection.commit()
    connection.close()

    return jsonify({
        'message': 'Data is deleted successfully.'
    })


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3002)
