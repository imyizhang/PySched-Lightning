#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Producer-consumer pattern, Scheduler."""

import collections


class Task(
    collections.namedtuple(
        'Task',
        'trigger, interval, time, priority, fn, args, kwargs, id'
    )
):
    __slots__ = []
    def __eq__(s, t): return (s.time, s.priority) == (t.time, t.priority)
    def __lt__(s, t): return (s.time, s.priority) <  (t.time, t.priority)
    def __le__(s, t): return (s.time, s.priority) <= (t.time, t.priority)
    def __gt__(s, t): return (s.time, s.priority) >  (t.time, t.priority)
    def __ge__(s, t): return (s.time, s.priority) >= (t.time, t.priority)


TIMEOUT = 3
TIMEFORMAT = '%Y-%m-%d %H:%M:%S %Z'

import abc
import time
import threading
import uuid

from .queue import PriorityQueue
from .executor import ThreadPoolExecutor, ProcessPoolExecutor
from .trigger import CronTrigger, RecurTrigger


class Scheduler(object):

    __metaclass__ = abc.ABCMeta

    _heart = None

    def __init__(self, executor=ThreadPoolExecutor(), timefunc=time.monotonic, delayfunc=time.sleep):
        super().__init__()
        self._queue = PriorityQueue()
        self._executor = executor
        self._lock = threading.RLock()
        self.now = timefunc
        self.idle = delayfunc
        self._stopped = True
        self._id = None
        self._task = {}
        self._result = {}

    @property
    def stopped(self):
        return self._stopped

    @property
    def task(self):
        return self._task

    @property
    def result(self):
        return self._result

    def delay(self, trigger, interval, priority, fn, args=(), kwargs={}, task_id=None):
        if trigger not in ['cron', 'recur']:
            raise ValueError('trigger must be "cron" or "recur"')
        self._id = task_id or uuid.uuid4().hex
        _trigger = self._create_trigger(trigger, self.now, interval)
        exe_time = _trigger.next_trigger_time()
        task = Task(trigger, interval, exe_time, priority, fn, args, kwargs, self._id)
        self._task[self._id] = task
        self._queue.put(task)
        return self._id

    def _create_trigger(self, trigger, timefunc, interval):
        if trigger == 'cron':
            _trigger = CronTrigger
        elif trigger == 'recur':
            _trigger = RecurTrigger
        trigger_kwargs = {'timefunc': timefunc, 'interval': interval}
        return _trigger.create(**trigger_kwargs)

    def cancel(self, task_id):
        if task_id in self._task:
            task = self._task.pop(task_id)
            self._queue.remove(task)
        else:
            raise ValueError('task_id {0} is invalid'.format(task_id))
        if task_id in self._result:
            self._result.pop(task_id)

    @abc.abstractmethod
    def start(self):
        self._stopped = False
        # localize variable access to minimize overhead
        # and to improve thread safety
        heartbeat = self._heartbeat
        self._heart = threading.Thread(target=heartbeat, name='heart')
        self._heart.daemon = True
        self._heart.start()

    def _heartbeat(self):
        while not self._stopped:
            task = self._queue.first()
            if task:  # i.e., queue.empty() -> False
                trigger, interval, exe_time, priority, fn, args, kwargs, task_id = task
                if exe_time > self.now():
                    self.idle(exe_time - self.now())
                else:
                    self._queue.get()  # pop the task
                    with self._lock:
                        try:
                            self._executor.run(fn, args, kwargs)
                            future = self._executor.future
                        except Exception:
                            break  # the last recurring execution would fail after shutdown
                    timestamp = time.strftime(TIMEFORMAT, time.localtime())
                    result = {'timestamp': timestamp, 'task': task, 'future': future}
                    if task_id in self._result:  # recurring execution
                        self._result[task_id].append(result)
                    else:  # the first execution
                        self._result[task_id] = [result]
                    _trigger = self._create_trigger(trigger, self.now, interval)
                    next_exe_time = _trigger.next_trigger_time(exe_time)
                    if next_exe_time:
                        self.delay(trigger, interval, priority, fn, args=args, kwargs=kwargs, task_id=task_id)
                    self.idle(0)  # let other threads run

    @abc.abstractmethod
    def shutdown(self, wait=True):
        self._stopped = True
        self._heart.join(timeout=TIMEOUT)
        del self._heart
        with self._lock:
            self._executor.shutdown(wait=wait)


class BackgroundScheduler(Scheduler):
    """A scheduler that runs in the background using a separate thread.
    BackgroundScheduler.start() will return immediately.
    """
    _event = None
    _thread = None

    def start(self):
        self._event = threading.Event()
        super().start()
        self._thread = threading.Thread(target=self._loop, name='background', args=(TIMEOUT,))
        self._thread.daemon = True
        self._thread.start()

    def _loop(self, timeout):
        while not self.stopped:
            self._event.wait(timeout=timeout)
            self._event.clear()

    def shutdown(self, wait=True):
        super().shutdown(wait=wait)
        self._event.set()
        self._thread.join()
        del self._thread
