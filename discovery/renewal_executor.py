# -*- coding: utf-8 -*-
# File   @ renewal_executor.py
# Create @ 2017/8/23 10:11
# Author @ 819070918@qq.com


#                   _ooOoo_
#                  o8888888o
#                  88" . "88
#                  (| -_- |)
#                  O\  =  /O
#               ____/`---'\____
#              .' \\|     |// '.
#             / \\|||  :  |||// \
#            / _||||| -:- |||||- \
#           |   | \\\  -  /// |   |
#           | \_|  ''\---/''  |_/ |
#           \  .-\__  '-'  ___/-. /
#         ___'. .'  /--.--\  '. .' ___
#      ."" '<  '.___\_<|>_/___.'  >' "".
#     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#     \  \ `-.   \_ __\ /__ _/   .-` /  /
# =====`-.____`-.___\_____/___.-`____.-'=====
#                   '=---='
#
# ===========================================
# ============ 佛祖保佑 == 永无BUG ============
# ===========================================

from eureka.utils.schedule.executor import Executor


class RenewalExecutor(Executor):

    def __init__(self, client, instance_info):
        self.client = client
        self.instance_info = instance_info

    def callable(self):
        self.instance_info.instance = self.client.query()
