# -*- coding: utf-8 -*-

"""Pool to execute calls asynchronously for scheduler,
ThreadPoolExecutor, ProcessPoolExecutor."""

import abc
import os
import concurrent.futures


class PoolExecutor(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, pool):
        super().__init__()
        self._pool = pool
        self._future = None

    @property
    def future(self):
        return self._future

    def run(self, fn, args=(), kwargs={}):
        self._future = self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True):
        self._pool.shutdown(wait=wait)


class ThreadPoolExecutor(PoolExecutor):

    def __init__(self, max_workers=os.cpu_count()):
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        super().__init__(pool)


class ProcessPoolExecutor(PoolExecutor):

    def __init__(self, max_workers=os.cpu_count()):
        pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        super().__init__(pool)
