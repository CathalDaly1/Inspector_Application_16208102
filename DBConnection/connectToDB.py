import sys
import psycopg2


def connectToDatabase():
    """
    This class creates a connection to postgresql database with a Heroku server for the application
    Connect to the database. Throw exception if the system cannot connect to the database.
    :return:
    """
    connectionString = 'postgres://hjzzzxkldardcd:7e4dd09652f3fafaa1f8af3701b741f8c4563ba06e1ea643670d82c758b8c493@ec2' \
                       '-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d7tfsem11o8afc'

    try:
        return psycopg2.connect(connectionString)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(0)
