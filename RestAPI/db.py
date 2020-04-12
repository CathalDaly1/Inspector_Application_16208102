import psycopg2
import psycopg2.extras

from flask import Flask

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

# close the cursor
cur.close()

# close the connection
conn.close()
