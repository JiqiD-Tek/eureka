# -*- coding: utf-8 -*-
# File   @ heart_beat_executor.py
# Create @ 2017/8/23 10:10
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


class HeartBeatExecutor(Executor):

    def __init__(self, client):
        self.client = client

    def callable(self):
        self.client.send_heart_beat()
