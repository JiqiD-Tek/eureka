# -*- coding: utf-8 -*-
# File   @ conf.py
# Create @ 2017/8/10 14:23
# Author @ 819070918@qq.com

import requests


EUREKA_INSTANCE_DEFINITION = {
    'needed': [
        'ipAddr', 'port', 'app'
    ],
    'needed-with-default': {
        'hostName': 'localhost',
        'port': 8761,
        'securePort': {
            '$': 443,
            '@enabled': 'false'
        },
        'dataCenterInfo': {
            'name': 'MyOwn',
            '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo'
        },
        'leaseInfo': {
            'durationInSecs': 30,
            'evictionDurationInSecs': 90,
        },
        'homePageUrl': "localhost",
        'healthCheckUrl': "localhost",
    },
    'transformations': [
        ('port', lambda p: is_number(p), lambda p: {'$': int(p), '@enabled': 'true'}),
        ('securePort', lambda p: is_number(p), lambda p: {'$': int(p), '@enabled': 'true'}),
    ]
}

EUREKA_HEADERS = {
    'POST': {'Content-Type': 'application/json'},
    'PUT': {},
    'GET': {'Accept': 'application/json'},
    'DELETE': {}
}

EUREKA_REQUESTS = {
    'POST': requests.post,
    'PUT': requests.put,
    'GET': requests.get,
    'DELETE': requests.delete
}


def is_number(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False
