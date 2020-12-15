#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Multi-producer, multi-consumer queues, Queue, PriorityQueue."""

import threading
import collections
import heapq


class Full(Exception):
    'Exception raised by Queue.put().'
    pass


class Queue(object):
    '''Queue object with a given maximum size.
    If max_size is <= 0, the queue size is infinite.
    '''

    def __init__(self, max_size=0):
        self._init(max_size)
        self.max_size = max_size
        self._lock = threading.RLock()

    def qsize(self):
        with self._lock:
            return self._qsize()

    def empty(self):
        with self._lock:
            return not self._qsize()

    def full(self):
        with self._lock:
            return 0 < self.max_size <= self._qsize()

    def put(self, item):
        with self._lock:
            if self.full():
                raise Full
            self._put(item)

    def get(self):
        with self._lock:
            if self.empty():
                return None
            return self._get()

    def first(self):
        with self._lock:
            if self.empty():
                return None
            return self._first()

    def remove(self, item):
        with self._lock:
            if self.empty():
                return None
            self._remove(item)

    # initialize the queue representation
    def _init(self, maxsize):
        self.queue = collections.deque()

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    # FIFO, leftmost first
    def _get(self):
        return self.queue.popleft()

    def _first(self):
        return self.queue[0]

    # remove the first occurrence of value
    def _remove(self, item):
        self.queue.remove(item)


class PriorityQueue(Queue):
    '''Variant of Queue where valued entries are retrieved in priority order (lowest first).
    Entries are typically tuples in the form of: (priority, value).
    '''

    # initialize the queue representation
    def _init(self, maxsize):
        self.queue = []

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        heapq.heappush(self.queue, item)

    def _get(self):
        return heapq.heappop(self.queue)

    def _first(self):
        return self.queue[0]

    # remove the first occurrence of value
    def _remove(self, item):
        self.queue.remove(item)
        heapq.heapify(self.queue)
