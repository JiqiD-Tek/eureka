# -*- coding: utf-8 -*-
# File   @ test.py
# Create @ 2017/8/11 15:59
# Author @ 819070918@qq.com

from __future__ import with_statement

from eureka import SimpleEurekaServiceWrapper
from eureka import SimpleEurekaClientWrapper

app = 'eureka-test'
eureka_urls = ['http://localhost:8761', ]
heartbeat = 5.0
instance = {
     'ipAddr': 'localhost',
     'port': 7777,
     'app': app,
     'instanceId': 'instanceId'
}


service_wrapper = SimpleEurekaServiceWrapper(eureka_urls, instance, heartbeat)

# Registering service
service_wrapper.run()
# Stopping service
service_wrapper.stop()

client_wrapper = SimpleEurekaClientWrapper(eureka_urls)

# Fetching app data
app_data = client_wrapper.app(app)

