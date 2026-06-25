import mysql.connector


def get_connection():

    connection = mysql.connector.connect(

        host="localhost",

        user="root",

        password="deep05",

        database="churn_db"

    )

    return connection