# coding: utf-8
import time


class Timeout(object):

    INTERVAL = 0.270  # 270 ms

    @staticmethod
    def hold_your_horses():
        time.sleep(Timeout.INTERVAL)

    @staticmethod
    def pause(interval):
        time.sleep(interval)
