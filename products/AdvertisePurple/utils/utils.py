import mysql
import mysql.connector

import logging
import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import requests

URL = "https://testing.purplyapp.com/sign-in"
USERNAME = "2011guptashalini@gmail.com"
PASSWORD = "Purply@1234"


def open_ssh_tunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.

   :param verbose: Set to True to show logging
   :return tunnel: Global SSH tunnel connection
   """

    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    global tunnel
    tunnel = SSHTunnelForwarder(ssh_address_or_host=('50.19.142.20', 22)
                                , ssh_username='ubuntu'
                                , ssh_pkey='C:/Users/gupta/Desktop/Advertise_Puple/key/ap-db-aws.pem'
                                , remote_bind_address=('advertise-purple-testing.cihesg5bocgi.us-east-1.rds.amazonaws.com', 3306)
                                )
    tunnel.start()


def mysql_connect():
    global connection
    local_bind_port = 0

    connection = pymysql.connect(
        host='127.0.0.1',
        user='advertise_purple',
        passwd='KXEHncaVuj3Gm76',
        db='advertise_purple',
        port=tunnel.local_bind_port
    )


def connect_db():
    open_ssh_tunnel()
    mysql_connect()


def run_query(sql):
    """Runs a given SQL query via the global database connection.
   """
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def mysql_disconnect():
    """Closes the MySQL database connection.
   """

    connection.close()


def close_ssh_tunnel():
    """Closes the SSH tunnel connection.
   """

    tunnel.close


def disconnect_db():
    mysql_disconnect()
    close_ssh_tunnel()


AFFILIATE_NAME = 'WICKFIRE LLC'
