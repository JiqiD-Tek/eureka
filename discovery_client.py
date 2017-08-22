# -*- coding: utf-8 -*-
# File   @ discovery_client.py
# Create @ 2017/8/10 14:22
# Author @ 819070918@qq.com

import eureka_http_client
import validator

from utils.schedule.handler import Handler
from utils.schedule.schedule_executor_service import ScheduleService


class HeartBeatHandler(Handler):

    def __init__(self, client):
        self.client = client

    def callable(self):
        self.client.send_heart_beat()


class RenewallHandler(Handler):

    def __init__(self, client, app_info):
        self.client = client
        self.app_info = app_info

    def callable(self):
        self.app_info["eureka"] = self.client.query()


class DiscoveryClient(object):

    def __init__(self, eureka_urls, instance_definition):

        if 'instanceId' not in instance_definition:
            instance_definition['instanceId'] = "{}:{}:{}".format(
                instance_definition['ipAddr'],
                instance_definition['app'],
                instance_definition['port'])
        self.instance_definition = validator.validate_instance_definition(instance_definition)

        self.client = eureka_http_client.EurekaHttpClient(eureka_urls, self.instance_definition)
        self.app_info = {"eureka": {}}

        self.schedule_service = ScheduleService()

        # 更新本地app数据
        self.schedule_service.schedule_at_fixed_rate("{}_RenewallHandler".
                                                     format(self.instance_definition["instance"]['instanceId']),
                                                     RenewallHandler(self.client, self.app_info),
                                                     self.instance_definition["instance"]["leaseInfo"]["durationInSecs"],
                                                     self.instance_definition["instance"]["leaseInfo"]["durationInSecs"])

    def register(self):
        """
          注册，并维持心跳服务
        """
        self.client.register()
        # 添加心跳
        self.schedule_service.schedule_at_fixed_rate("{}_HeartBeatHandler"
                                                     .format(self.instance_definition["instance"]['instanceId']),
                                                     HeartBeatHandler(self.client),
                                                     0,
                                                     self.instance_definition["instance"]["leaseInfo"]["durationInSecs"])

    def deregister(self):
        """
          注销服务
        """
        # 注销心跳
        self.schedule_service.drop_schedule("{}_HeartBeatHandler"
                                            .format(self.instance_definition["instance"]['instanceId']))
        self.client.cancel()

    def app(self, app_name):
        """
          获取服务详情
        """
        application_list = self.app_info["eureka"]["applications"].get("application", [])

        for item in application_list:
            if item["name"] == app_name:
                return {"application": item}

        return None
