# -*- coding: utf-8 -*-
from flask import Flask, render_template, json, request, Response, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import closing
import pymysql

mysql = MySQL()
app = Flask(__name__, static_url_path='/static')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'motorola_motox4'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def connection():
    # Edited out actual values
    conn = mysql.connect(host="localhost",
                         user="root",
                         passwd="motorola_motox4",
                         db = "BucketList")
    cursor = conn.cursor()

    return cursor, conn

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            #cursor = mysql.connection.cursor()

            # added - JMM - 2019/02/07
            #with closing(mysql.connect()) as conn:
            #    with closing(conn.cursor()) as cursor:
            query = "select * from BucketList.tbl_user where user_email = %s"
            cursor.execute(query, (_email))
            data = cursor.fetchall()

            try:
                conn1 = mysql.connect()
                cursor1 = conn1.cursor()
                # cursor1 = mysql.connection.cursor()

                # with closing(mysql.connect()) as conn1:
                #    with closing(conn.cursor()) as cursor1:
                _hashed_password = generate_password_hash(_password)
                query2 = "insert into BucketList.tbl_user (user_name,user_email,user_password) values (%s,%s,%s)"

                cursor1.execute(query2, (_name, _email, _hashed_password))

                if len(data) is 0:

                   conn1.commit()

                   return json.dumps({'message':'User created successfully !'})
                   return json.dumps({'html': '<h4>User Created: </h4></br></br>'})
                   return json.dumps({'html': '<p>'+str(_name)+'</p>'})

                else:
                    return json.dumps({'data error':str(data[0]),
                                       'message': 'An account associated with this email address already exists.'})
                    return json.dumps({'html': '<span>An account associated with this email address already exists.</span>'})

                #origin - NO SIRVE
                #_hashed_password = generate_password_hash(_password)
                #cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
                #data = cursor.fetchall()

            except Exception as e:
                return json.dumps({'error exception': str(e)})

            finally:
                cursor1.close()
                conn1.close()

            #return render_template("consulta.html", data=data)

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
            return json.dumps({'message': 'Enter the required fields: '})
            return json.dumps({'message': str(_name)})
            return json.dumps({'message': str(_email)})
            return json.dumps({'message': str(_password)})
            print('Enter the required fields:', str(_name), ", ", str(_email), ', ', str(_password))

    except Exception as e:
        return json.dumps({'error exception':str(e)})
    finally:
        cursor.close()
        conn.close()

def conexion():
    host = "127.0.0.1"
    user = "root"
    password = "motorola_motox4"
    db = "BucketList"
    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()

    return cur

def list_users():
    cursor = conexion()
    cursor.execute("select user_id, user_name, user_email from BucketList.tbl_user")
    result = cursor.fetchall()
    return result


@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    def db_query():
        # db = __init__(self=self)
        users = list_users()
        return users

    res = db_query()

    # return json.dumps({'data query': str(res[0])})

    return render_template('consulta.html', result=res, content_type='application/json')

if __name__ == "__main__":
    app.run(debug=True)


'''
@app.route('/consulta', methods=['POST', 'GET'])
def result():
    try:

        if request.method == "POST":
            #cursor, conn = connection()

            #conn = mysql.connect()
            #cursor = conn.cursor()
            # cursor = mysql.connection.cursor()

            # added - JMM - 2019/02/07
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    query = "select * from BucketList.tbl_user"
                    cursor.execute(query)

                    rows = cursor.fetchall()

                    row_headers = [x[0] for x in cursor.description]  # this will extract row
                    # headers

                    json_data = []
                    for result in rows:
                        json_data.append(dict(zip(row_headers, result)))

                    consultajs = json.dumps(json_data)

                    resp = Response(consultajs, status=200, mimetype='application/json')
                    #resp.headers['Link'] = 'consulta.html'

                    return json.dumps({'sql data: ': str(rows[0])})

                    #return render_template("consulta.html", str(rows[0])=str(rows[0]))

                    #return render_template("consulta.html", records=cursor.fetchall())

                    #for data in cursor.fetchall():
                        #return data, {'Content-Type': 'text/html'}
                    #    return redirect(url_for('consulta'))

        #return render_template("consulta.html")

    except Exception as e:
        return json.dumps({'error exception': str(e)})
'''

