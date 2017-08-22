# -*- coding: utf-8 -*-
# File   @ django.py
# Create @ 2017/8/10 14:21
# Author @ 819070918@qq.com

from __future__ import absolute_import
from django.conf import settings

from eureka import defaults

from eureka import DiscoveryClient


client = None

if client is None:
    eureka_urls = getattr(settings, 'EUREKA_URLS', defaults.EUREKA_URLS)
    instance = getattr(settings, 'INSTANCE', defaults.INSTANCE)

    client = DiscoveryClient(eureka_urls, instance)
    client.register()


