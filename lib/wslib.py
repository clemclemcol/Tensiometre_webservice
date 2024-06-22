import pymysql
import sys
import cgi
import os
import json

url = 'https://www.gaalactic.fr/~colnotc/ws/messages'
customHeaders = {'Accept': 'application/json', 'User-agent': 'my_client_agent/v0.0.1'}



def validate_request():
    method = os.environ.get('REQUEST_METHOD', '')
    if method not in ['GET', 'POST', 'PUT', 'DELETE']:
        print('Content-type: application/json\n')
        print(json.dumps({"error": "Invalid request method"}))
        sys.exit()



def return_http_data():
    print(os.environ['REQUEST_METHOD'])
    if os.environ['REQUEST_METHOD'] in ['POST', 'DELETE']:
        try:
            print("pre cast")
            request_body_size = int(os.environ.get('CONTENT_LENGTH', 0))
            print("post cast")

        except (ValueError):
            print("error cast")
            request_body_size = 0
            
        print(request_body_size)
        request_body = sys.stdin.read(request_body_size)

        if(os.environ['REQUEST_METHOD'] == 'DELETE'):
            data = json.loads(request_body)
        else:
            jsonString = "{"
            bodymap = request_body.split("&")
            count = 0
            for item in bodymap : 
                count = count+1
                split = item.split("=")
                jsonString = jsonString + "\""+ split[0]+"\"" + ":" +"\""+ split[1]+"\""
                if(count!=len(bodymap)):
                    jsonString = jsonString + ","
            jsonString = jsonString + "}"
            print(jsonString)
            data = json.loads(jsonString)
        print(data)
        return data
    else:
        formData = cgi.FieldStorage()
        httpData = {}
        for key in formData.keys():
            httpData[key] = formData.getvalue(key)
        return httpData
    
    
def connect_db_tuto():
    return pymysql.connect(
        host='localhost',
        user='colnotc',
        password='@23vdzB8#H',
        db='colnotc',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def read_all_resources():
    connection = connect_db_tuto()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `messages`"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()

def read_resource(data):
    dest = data.get('dest')
    connection = connect_db_tuto()
    try:
        with connection.cursor() as cursor:
            if dest:
                sql = "SELECT * FROM `messages` WHERE `dest`=%s"
                cursor.execute(sql, (dest,))
            else:
                return {
                    "code": "OPERATION_OK",
                    "operation": "COLLECTION_READ",
                    "text": "Collection read successful",
                    "content": read_all_resources()
                }
            result = cursor.fetchall()
        if result:
            return {
                "code": "OPERATION_OK",
                "operation": "COLLECTION_READ",
                "text": "Collection read successful",
                "content": result
            }
        else:
            return {
                "code": "OPERATION_KO",
                "operation": "RESOURCE_READ",
                "text": "Resource not found",
                "content": read_all_resources()
            }
    finally:
        connection.close()

def add_resource(data):
    dest = data.get('dest')
    print(dest)

    message = data.get('message')
    print(message)

    if not dest or not message:
        print(message)

        return {
            "code": "OPERATION_KO",
            "operation": "RESOURCE_ADD",
            "text": "Missing 'dest' or 'message' parameter"
        }

    connection = connect_db_tuto()
    print(connection)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `messages` (`dest`, `text`) VALUES (%s, %s)"
            print(sql)
            cursor.execute(sql, (dest, message))
            connection.commit()
        return {
            "code": "OPERATION_OK",
            "operation": "RESOURCE_ADD",
            "text": "Message added",
            "id": cursor.lastrowid
        }
    except Exception as inst:

        print(type(inst))    # the exception type
    
        print(inst.args)     # arguments stored in .args
    
        print(inst)   
    finally:
        connection.close()
        
def update_resource(data):
    dest = data.get('dest')
    message = data.get('message')
    if not dest or not message:
        return {
            "code": "OPERATION_KO",
            "operation": "RESOURCE_UPDATE",
            "text": "Missing 'dest' or 'message' parameter"
        }

    connection = connect_db_tuto()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `messages` SET `text`=%s WHERE `dest`=%s"
            print(sql)
            cursor.execute(sql, (message,dest))
            connection.commit()
        return {
            "code": "OPERATION_OK",
            "operation": "RESOURCE_ADD",
            "text": "Message added",
            "id": cursor.lastrowid
        }
    finally:
        connection.close()

def delete_resource(data):
    dest = data.get('dest')
    if not dest:
        return {
            "code": "OPERATION_KO",
            "operation": "RESOURCE_DELETE",
            "text": "Missing 'dest' parameter"
        }

    connection = connect_db_tuto()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `messages` WHERE `dest`=%s"
            rows_deleted = cursor.execute(sql, (dest,))
            connection.commit()
        if rows_deleted:
            return {
                "code": "OPERATION_OK",
                "operation": "RESOURCE_DELETE",
                "text": "Resource delete successful",
                "content": read_all_resources()
            }
        else:
            return {
                "code": "DELETE_KO",
                "operation": "RESOURCE_DELETE",
                "text": "Resource not found",
                "content": read_all_resources()
            }
    finally:
        connection.close()

