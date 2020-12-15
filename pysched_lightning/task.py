#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


# task class as decorator
class task(object):

    def __init__(self, scheduler, trigger, interval, priority):
        self.scheduler = scheduler
        self.trigger = trigger
        self.interval = interval
        self.priority = priority

    def __call__(self, fn):
        @functools.wraps(fn)
        def delay(*args, **kwargs):
            return self.scheduler.delay(self.trigger, self.interval, self.priority,
                                        fn, args=args, kwargs=kwargs)
        fn.delay = delay
        return fn
