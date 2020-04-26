import unittest
from DBConnection.connectToDB import *


class test_connectToDB(unittest.TestCase):
    def testDBConnection(self):
        connectionString = 'postgres://hjzzzxkldardcd:7e4dd09652f3fafaa1f8af3701b741f8c4563ba06e1ea643670d82c758b8c493@ec2' \
                           '-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d7tfsem11o8afc'
        try:
            return psycopg2.connect(connectionString)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
