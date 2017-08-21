# -*- coding: utf-8 -*-
# File   @ ratelimit.py
# Create @ 2017/8/21 19:54
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


class Clock(object):
    """docstring for Clock"""

    def now(self):
        return int(time.time() * 1000000)

    def sleep(self, duration):
        time.sleep(float(duration) / 1000000)


infinity_duration = 10000000000000


class Bucket(object):
    """docstring for Bucket"""

    def __init__(self, start_time, capacity, quantum, fill_interval, clock, avail):

        self.start_time = start_time
        self.capacity = capacity
        self.quantum = quantum
        self.fill_interval = fill_interval
        self.clock = clock

        self.avail = avail
        self.avail_tick = 0

        self.mu = threading.Lock()

    def wait(self, count):
        """
        """
        d, ok = self.take(self.clock.now(), count, infinity_duration)
        if d > 0:
            self.clock.sleep(d)

    def wait_max_duration(self, count ,max_wait):
        """
        """
        d, ok = self.take_max_duration(count, max_wait)
        if d > 0:
            self.clock.sleep(d)

    def take_max_duration(self, count, max_wait):
        """
        """
        return self.take(self.clock.now(), count, max_wait)

    def take(self, now, count, max_wait):
        """
         获取令牌，并添加最大等待时间
        """

        if count <= 0:
            return 0, True

        with self.mu:
            current_tick = self.adjust(now)
            avail = self.avail - count
            if avail >= 0:
                self.avail = avail
                return 0, True

            end_tick = current_tick + (-avail+self.quantum-1)/self.quantum
            end_time = self.start_time + end_tick * self.fill_interval
            wait_time = end_time - now

            if wait_time > max_wait:
                return 0, False

            self.avail = avail
            return wait_time, True

    def take_available(self, count):
        """
         获取count 的令牌
        """

        if count <= 0:
            return

        with self.mu:
            self.adjust(self.clock.now())

            if self.avail <= 0:
                return 0

            if count > self.avail:
                count = self.avail

            self.avail -= count

        return count

    def adjust(self, now):
        """
        根据时间调整参数
        """
        current_tick = (now-self.start_time)/self.fill_interval

        if self.avail >= self.capacity:
            return current_tick

        self.avail += (current_tick - self.avail_tick) * self.quantum

        if self.avail > self.capacity:
            self.avail = self.capacity

        self.avail_tick = current_tick

        return current_tick

    def available(self):
        """
        """
        with self.mu:
            self.adjust(self.clock.now())

        return self.avail

    def capacity(self):
        """
        """
        return self.capacity


def new_bucket(fill_interval, capacity):
    """
    """
    return new_bucket_with_clock(fill_interval, capacity, Clock())


def new_bucket_with_clock(fill_interval, capacity, clock):
    """
    """
    return new_bucket_with_quantum_and_clock(fill_interval, capacity, 1, clock)


def new_bucket_with_rate(rate, capacity):
    """
    """
    return new_bucket_with_rate_and_clock(rate, capacity, Clock())


def new_bucket_with_rate_and_clock(rate, capacity, clock):
    """
    """
    pass


def new_bucket_with_quantum(fill_interval, capacity, quantum):
    """
    """
    return new_bucket_with_quantum_and_clock(fill_interval, capacity, quantum, Clock())


def new_bucket_with_quantum_and_clock(fill_interval, capacity, quantum, clock):
    """
    """
    if fill_interval <= 0:
        raise Exception("token bucket fill interval is not > 0")

    if capacity <= 0:
        raise Exception("token bucket capacity is not > 0")

    if quantum <= 0:
        raise Exception("token bucket quantum is not > 0")

    return Bucket(clock.now(), capacity, quantum, fill_interval, clock, capacity)
