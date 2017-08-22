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

    def __init__(self, task_id, handler, timestamp, period):
        threading.Thread.__init__(self)
        self.task_id = task_id
        self.handler = handler
        self.timestamp = timestamp
        self.period = period

    def run(self):
        """
        """
        self.handler.callable()


execute_service_lock = threading.Lock()


class ExecuteService(threading.Thread):
    """docstring for ScheduleExecuteService"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.link = Link()

    def run(self):
        while True:
            p = self.link.head
            while p.next and p.next.data.timestamp < now():
                p.next.data.start()
                if p.next.data.period > 0:
                    self.add(Task(p.next.data.task_id,
                                  p.next.data.handler,
                                  p.next.data.timestamp + p.next.data.period,
                                  p.next.data.period))

                execute_service_lock.acquire()
                p.next = p.next.next
                execute_service_lock.release()

            time.sleep(1)

    def add(self, task):
        """
          添加定时任务
        """
        execute_service_lock.acquire()
        p = self.link.head
        while p.next and p.next.data.timestamp < task.timestamp:
            p = p.next

        new = Node(task, p.next)
        p.next = new

        execute_service_lock.release()

    def remove(self, task_id):
        """
          删除定时任务
        """
        execute_service_lock.acquire()
        p = self.link.head

        while p.next and p.next.data.task_id != task_id:
            p = p.next

        if p.next:
            p.next = p.next.next
        execute_service_lock.release()


class ScheduleService(object):

    def __init__(self):
        self.execute = ExecuteService()
        self.execute.setDaemon(True)
        self.execute.start()

    def schedule(self, task_id, handler, delay):
        """
        """
        self.execute.add(Task(task_id, handler, now() + delay, 0))

    def schedule_at_fixed_rate(self, task_id, handler, init_delay, period):
        """
        """
        self.execute.add(Task(task_id, handler, now() + init_delay, period))

    def drop_schedule(self, task_id):
        """
        """
        self.execute.remove(task_id)
