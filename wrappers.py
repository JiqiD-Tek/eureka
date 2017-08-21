# -*- coding: utf-8 -*-
# File   @ wrappers.py
# Create @ 2017/8/10 14:22
# Author @ 819070918@qq.com

import time
import client
import threading


class SimpleEurekaClientWrapper:
    def __init__(self, eureka_urls):
        self.client = client.EurekaClient(eureka_urls)

    def app(self, app_name):
        return self.client.query(app=app_name)

    def instance(self, instance, app_name=None):
        return self.client.query(app=app_name, instance=instance)


class SimpleEurekaServiceWrapper:
    def __init__(self, eureka_urls, instance_definition, heartbeat_interval):
        self.client = client.EurekaClient(eureka_urls, instance_definition)
        self.heartbeat_interval = heartbeat_interval

    def run(self):
        self.client.register()
        heart_beat_thread = HeartBeatThread(self.client, self.heartbeat_interval)
        heart_beat_thread.setDaemon(True)
        heart_beat_thread.start()

    def stop(self):
        self.client.deregister()


class HeartBeatThread(threading.Thread):
    def __init__(self, eureka_client, heartbeat_interval):
        threading.Thread.__init__(self)
        self.eureka_client = eureka_client
        self.heartbeat_interval = heartbeat_interval

    def run(self):
        while True:
            self.eureka_client.heartbeat()
            time.sleep(self.heartbeat_interval)
