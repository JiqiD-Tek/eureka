# -*- coding: utf-8 -*-
# File   @ discovery_client.py
# Create @ 2017/8/10 14:22
# Author @ 819070918@qq.com

import configure
from eureka.discovery.eureka_http_client import EurekaHttpClient
from eureka.discovery.heart_beat_executor import HeartBeatExecutor
from eureka.discovery.renewal_executor import RenewalExecutor
from eureka.utils.schedule.schedule_executor_service import ScheduleService


class DiscoveryClient(object):

    def __init__(self, eureka_urls, instance_definition):

        self.instance_definition = self.validator(instance_definition)

        self.schedule = ScheduleService()

        self.query_client = EurekaHttpClient(eureka_urls, self.instance_definition)
        self.instance_info = {"eureka": {}}

        self.renewal_executor = RenewalExecutor(self.query_client, self.instance_info)
        self.heart_beat_executor = HeartBeatExecutor(self.query_client)

        # 更新本地app数据
        self.schedule.schedule_at_fixed_rate("{}_RenewalExecutor".
                                             format(self.instance_definition["instance"]['instanceId']),
                                             self.renewal_executor,
                                             0,
                                             self.instance_definition["instance"]["leaseInfo"]["durationInSecs"])

    def validator(self, instance_definition):
        """
          参数校验
        """
        if 'instanceId' not in instance_definition:
            instance_definition['instanceId'] = "{}:{}:{}".format(
                instance_definition['ipAddr'],
                instance_definition['app'],
                instance_definition['port'])

        for needed in configure.EUREKA_INSTANCE_DEFINITION['needed']:
            if needed not in instance_definition:
                raise Exception("{} is necessary".format(needed))

        configure.EUREKA_INSTANCE_DEFINITION['needed-with-default'].update(instance_definition)
        instance_definition = configure.EUREKA_INSTANCE_DEFINITION['needed-with-default']

        for part in configure.EUREKA_INSTANCE_DEFINITION['transformations']:
            if part[0] in instance_definition and part[1](instance_definition[part[0]]):
                instance_definition[part[0]] = part[2](instance_definition[part[0]])

        return {'instance': instance_definition}

    def register(self):
        """
          注册服务
        """
        self.query_client.register()
        # 添加心跳
        self.schedule.schedule_at_fixed_rate("{}_HeartBeatExecutor"
                                             .format(self.instance_definition["instance"]['instanceId']),
                                             self.heart_beat_executor,
                                             0,
                                             self.instance_definition["instance"]["leaseInfo"]["durationInSecs"])

    def renew(self):
        """
        """
        pass

    def unregister(self):
        """
          注销服务
        """
        # 删除心跳
        self.schedule.drop_schedule("{}_HeartBeatExecutor".format(self.instance_definition["instance"]['instanceId']))
        self.query_client.cancel()

    def get_applications(self):
        """
        """
        return self.instance_info["eureka"]

    def get_application(self, app_name):
        """
          获取服务详情
        """
        application_list = self.instance_info["eureka"].get("applications", {}).get("application", [])

        for item in application_list:
            if item["name"] == app_name:
                return {"application": item}

        return None
