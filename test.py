# -*- coding: utf-8 -*-
# File   @ test.py
# Create @ 2017/8/11 15:59
# Author @ 819070918@qq.com

from __future__ import with_statement


from eureka import DiscoveryClient

app = 'eureka-test'

eureka_urls = ['http://localhost:8761', ]

instance = {
     'ipAddr': 'localhost',
     'port': 7777,
     'app': app,
     'instanceId': 'instanceId',
     'leaseInfo': {
          'durationInSecs': 10,
          'evictionDurationInSecs': 20,
     }
}


client = DiscoveryClient(eureka_urls, instance)

# Registering service
client.register()
# Stopping service
client.deregister()

# Fetching app data
app_data = client.app(app)

