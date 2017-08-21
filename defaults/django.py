# -*- coding: utf-8 -*-
# File   @ django.py
# Create @ 2017/8/10 14:21
# Author @ 819070918@qq.com

from __future__ import absolute_import
from django.conf import settings

from eureka import defaults
from eureka import SimpleEurekaServiceWrapper


service_wrapper = None

if service_wrapper is None:
    eureka_urls = getattr(settings, 'EUREKA_URLS', defaults.EUREKA_URLS)
    instance = getattr(settings, 'INSTANCE', defaults.INSTANCE)
    heartbeat = getattr(settings, 'HEARTBEAT', defaults.HEARTBEAT)
    service_wrapper = SimpleEurekaServiceWrapper(eureka_urls, instance, heartbeat)
    service_wrapper.run()


