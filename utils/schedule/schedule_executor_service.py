# -*- coding: utf-8 -*-
# File   @ schedule_executor_service.py
# Create @ 2017/8/21 20:09
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

import time
import threading


def now():
    return int(time.time())


class Node(object):
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Link(object):
    """docstring for Link"""

    def __init__(self):
        self.head = Node(None, None)


class Task(threading.Thread):

    def __init__(self, command, timestamp, period):
        threading.Thread.__init__(self)
        self.command = command
        self.timestamp = timestamp
        self.period = period

    def run(self):
        """
        """
        self.command()


class ExecuteService(threading.Thread):
    """docstring for ScheduleExecuteService"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.link = Link()

    def run(self):
        while True:
            p = self.link.head
            while not p.next and p.next.data.timestamp < now():
                p.next.data.start()
                if p.next.data.period > 0:
                    self.add(Task(p.next.data.command, p.next.data.timestamp + p.next.data.period, p.next.data.period))

                p.next = p.next.next

            time.sleep(1)

    def add(self, task):
        """
        """
        p = self.link.head
        while not p.next and p.next.data.timestamp < task.timestamp:
            p = p.next

        new = Node(task, p.next)
        p.next = new


class ScheduleService(object):

    def __init__(self):
        self.execute = ExecuteService()
        self.execute.setDaemon(True)
        self.execute.start()

    def schedule(self, command, delay):
        """
        """
        self.execute.add(Task(command, now() + delay, 0))

    def schedule_at_fixed_rate(self, command, init_delay, period):
        """
        """
        self.execute.add(Task(command, now() + init_delay, period))

    def schedule_with_fixed_rate(self, command, init_delay, period):
        """
        """
        self.execute.add(Task(command, now() + init_delay, period))
