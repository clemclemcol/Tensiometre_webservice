#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('Content-type: application/json\n')

import json

data = {
    "01-info": {
        "version": 1,
        "collection_name": "messages",
        "collection_URI": "https://www.gaalactic.fr/~colnotc/ws/messages",
        "title": "Messages Web Service",
        "host": "www.gaalactic.fr",
        "description": "Returns targeted Hello messages",
        "base_path": "/~colnotc/ws"
    },
    "02-methods": {
        "POST": "yes",
        "DELETE": "yes",
        "PUT": "yes",
        "GET": "yes"
    },
    "03-headers": {
        "consumes": {
            "Content type": ["application/x-www-form-urlencoded"],
            "Accept": ["application/json", "text/html"]
        },
        "produces": {
            "Content type": ["application/json", "text/html"]
        }
    }
}

print(json.dumps(data))
