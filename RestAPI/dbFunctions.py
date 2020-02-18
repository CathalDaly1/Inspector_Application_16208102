import psycopg2
import psycopg2.extras
import json

from flask import Flask, render_template, request

app = Flask(__name__)


def connectToDB():
    connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
    print(connectionString)
    try:
        print("Connected successfully")
        return psycopg2.connect(connectionString)
    except:
        print("Cannot connect to the DB")


conn = connectToDB()
cur = conn.cursor()


def test():
    username
    cur.execute("SELECT * FROM Users WHERE username = 'test'")
    rows = cur.fetchall()

    for row in rows:
        print("Uid: ", row[0])
        print("Username: ", row[1])
        print("Password: ", row[2])

def executeQuery(query):
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data_inner = []
    for result in rv:
        json_data_inner.append(dict(zip(row_headers, result)))
    json_dict = {"results": json_data_inner}
    return json.dumps(json_dict)


def executeQueryParameterised(query, param):
    cur.execute(query, (param,))
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data_inner = []
    for result in rv:
        json_data_inner.append(dict(zip(row_headers, result)))
    json_dict = {"results": json_data_inner}
    return json.dumps(json_dict)


def insert(query):
    print(query)
    cur.execute(query)
    conn.commit()
    return 200


def delete(query):
    cur.execute(query)
    conn.commit()
    return 200
