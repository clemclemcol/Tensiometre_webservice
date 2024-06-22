#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extended client agent script to handle GET, POST, PUT and DELETE requests
"""

import requests
import json

# Function to send a GET request
def send_get_request(url, headers, dest=None):
    if dest:
        url = f"{url}/{dest}"
    response = requests.get(url, headers=headers)
    print_response(response)

# Function to send a POST request
def send_post_request(url, headers, dest, message):
    data = {'dest': dest, 'message': message}
    response = requests.post(url, headers=headers, data=data)
    print_response(response)
    
# Function to send a PUT request
def send_put_request(url, headers, dest, message):
    data = {'dest': dest, 'message': message}
    response = requests.put(url, headers=headers, data=data)
    print_response(response)

# Function to send a DELETE request
def send_delete_request(url, headers, dest):
    data = {'dest': dest}
    response = requests.delete(url, headers=headers, data=json.dumps(data))
    print_response(response)   

# Function to print the response from the server
def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Headers:", response.headers)
    print("Content:", response.text)

def main():
    # URL of the resource
    url = 'https://www.gaalactic.fr/~colnotc/ws/messages'

    # Ask user for credentials
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    # Prepare authorization header
    auth_value = f"{username}:{password}"
    customHeaders = {
        'Accept': 'application/json',
        'User-agent': 'my_client_agent/v0.0.1',
        'X-Auth': auth_value,
        'Content-type': 'application/x-www-form-urlencoded'
    }

    # Ask user for the type of request to send
    request_type = input("Enter request type (GET/POST/PUT/DELETE): ").strip().upper()

    if request_type == 'GET':
        dest = input("Enter the destination (or leave empty to get all): ").strip()
        send_get_request(url, customHeaders, dest)
    elif request_type == 'POST':
        dest = input("Enter destination: ").strip()
        message = input("Enter message: ").strip()
        send_post_request(url, customHeaders, dest, message)
    elif request_type == 'PUT':
        dest = input("Enter destination: ").strip()
        message = input("Enter message: ").strip()
        send_put_request(url, customHeaders, dest, message)
    elif request_type == 'DELETE':
        dest = input("Enter the destination to delete: ").strip()
        send_delete_request(url, customHeaders, dest)
    else:
        print("Invalid request type. Please enter GET, POST, or DELETE.")

if __name__ == "__main__":
    main()
