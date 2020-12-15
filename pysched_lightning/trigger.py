#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Triggers for scheduler, CronTrigger, RecurTrigger."""

import abc


class Trigger(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, timefunc, interval):
        super().__init__()
        #os.environ['TZ'] = 'CET'
        #time.tzset()
        self.now = timefunc
        self.interval = interval
        self.start = self.now()

    @classmethod
    def create(cls, **trigger_kwargs):
        return cls(**trigger_kwargs)

    @abc.abstractmethod
    def next_trigger_time(self, previous_trigger_time):
        raise NotImplementedError


class CronTrigger(Trigger):

    def next_trigger_time(self, previous_trigger_time=None):
        if not previous_trigger_time:
            return self.start + self.interval
        return None


class RecurTrigger(Trigger):

    def next_trigger_time(self, previous_trigger_time=None):
        if not previous_trigger_time:
            return self.start + self.interval
        return previous_trigger_time + self.interval
