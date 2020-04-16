# coding: utf-8
import time


class Timeout(object):

    INTERVAL = 0.050  # 50 ms

    @staticmethod
    def hold_your_horses():
        time.sleep(Timeout.INTERVAL)
