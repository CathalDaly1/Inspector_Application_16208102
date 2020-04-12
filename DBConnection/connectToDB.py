import sys

import psycopg2


def connectToDB():
    """
    This class creates a connection to postgresql database for the application
    :return:
    """
    connectionString = 'dbname=InspectorFYP_DB user=postgres password=Detlef228425 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(0)
