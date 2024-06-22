#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import pymysql
import cgi
import cgitb

cgitb.enable()  # Enable CGI error reporting

sys.path.insert(1, '/home/colnotc/public_html/ws/lib')
import wslib


# Function to get and verify credentials from Authorization header
def get_credentials():
    auth_header = os.environ.get('HTTP_X_AUTH')
    if not auth_header:
        return None, None
    username, password = auth_header.split(':', 1)
    return username, password

# Verify user credentials and get user rights
def verify_credentials(username, password):
    connection = wslib.connect_db_tuto()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `rights` FROM `users` WHERE `loginUser` = %s AND `pwdUser` = PASSWORD(%s)"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return result['rights']
            return None
    finally:
        connection.close()
        
print('Content-type: application/json\n\n')

try:
    print("1")
    # Validate the request
    wslib.validate_request()
    print("2")


    # Get credentials
    username, password = get_credentials()
    print("3")


    if not username or not verify_credentials(username, password):
        print(json.dumps({"error": "Unauthorized"}))
        sys.exit()
    print("4")

    # Get user rights
    rights = verify_credentials(username, password)
    print("5")


    # Get the request method
    method = os.environ.get('REQUEST_METHOD', '')
    print("6")


    # Get the data from the request
    data = wslib.return_http_data()
    print("7")


    # Check user rights and handle the request based on the method
    if method == 'GET':
        print("GET")

        if rights in ['read', 'all']:
            response = wslib.read_resource(data)
        else:
            response = {"error": "Operation not allowed"}
    elif method == 'POST':
        print("POST")

        if rights == 'all':
            print("8.1")

            response = wslib.add_resource(data)
        else:
            print("8.2")

            response = {"error": "Operation not allowed"}
    elif method == 'PUT':
        print("PUT")

        if rights == 'all':
            response = wslib.update_resource(data)
        else:
            response = {"error": "Operation not allowed"}
    elif method == 'DELETE':
        print("DELETE")

        if rights == 'all':
            response = wslib.delete_resource(data)
        else:
            response = {"error": "Operation not allowed"}
    else:
        response = {"error": "Invalid request method"}
    print("9")

    # Send the JSON response
    print(json.dumps(response))
    print("10")

except Exception as e:

    print(json.dumps({"error": "Internal Server Error", "message": str(e)}))
    sys.exit()
