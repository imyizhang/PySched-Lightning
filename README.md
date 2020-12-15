# PySched-Lightning

PySched-Lightning is

* a lightweight task queue scheduler that runs in the background
* written in [Python (3.7+) Standard Library](https://docs.python.org/3.7/library/)



PySched-Lightning supports to

* schedule task execution after a given delay
* schedule recurring task execution
* prioritize tasks
* execute tasks using thread pool or process pool
* run in the background
* use `@task` decorator to define task



## Quickstart

Define your function, `now(cost)` as an example:

```python
import time

def now(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )
    
def utcnow(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()) )
```

Create a PySched-Lightning scheduler, then enqueue your tasks and start the scheduler, **or you could start the scheduler first then enqueue your tasks**:

```python
import pysched-lightning

sched = pysched-lightning.Scheduler()
sched.delay(trigger='recur', interval=3, priority=2, fn=now, args=(1,))
sched.delay(trigger='recur', interval=2, priority=1, fn=utcnow, args=(1,))
sched.start()
```

Shutdown the scheduler:

```python
sched.shutdown(wait=True)
```



### Play with the `@task` decorator

Use `@task` decorator to define your function, then schedule it and start the scheduler, `now(cost)` as an example:

```python
import pysched-lightning

sched = pysched-lightning.Scheduler()
sched.start()

import time

@pysched-lightning.task(sched, 'recur', 3, 2)
def now(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()) )

now.delay(cost=1)    
    
@pysched-lightning.task(sched, 'recur', 2, 1)
def utcnow(cost=1):
    time.sleep(cost)
    print( time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()) )
    
utcnow.delay(cost=1)
```

When you'd like to cancel the recurring execution, shutdown the scheduler as usual:

```python
sched.shutdown(wait=True)
```



### Install PySched-Lightning

```bash
$ pip install pysched-lightning
```



## Documentation

### `ThreadPoolExecutor`/`ProcessPoolExecutor`

```python
class pysched-lightning.ThreadPoolExecutor/ProcessPoolExecutor(max_workers=<num_cpu_cores>)
```

`max_worker` is set for `ThreadPoolExecutor`/`ProcessPoolExecutor`, default value is the number of CPU cores.

* `future`

  [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object

* `run(fn, args=(), kwargs={})`

  Execute the function using thread pool or process pool.

* `shutdown(wait=True)`

  Shutdown the executor.



### `Scheduler`

```python
class pysched-lightning.Scheduler(executor=ThreadPoolExecutor(), timefunc=time.monotonic, delayfunc=time.sleep)
```

Default executor is a thread pool. `timefunc` should be callable without arguments, and return a number, the time at the moment. `delayfunc` should be callable with one argument, compatible with the output of `timefunc`, and should delay that many time units (seconds as default time unit).

* `stopped`

  The scheduler is stopped or not, `True` (default) or `False`.

* `task`

  The task id, `Task` object (`collections.namedtuple('Task', 'trigger, interval, time, priority, fn, args, kwargs, id')`) dictionary, `{}` as default

* `result`

  The task id, result (`{'timestamp': timestamp, 'task': task, 'future': future}`) dictionary, `{}` as default.

* `delay(trigger, interval, priority, fn, args=(), kwargs={})`

  `trigger` must be `'cron'` or `'recur'`. Enqueue the task, schedule the execution and return a corresponding id.

* `start()`

  Let scheduler start in the background.

* `cancel(task_id)`

  Cancel a certain task with its id.

* `shutdown(wait=True)`

  Shutdown the scheduler.



### `task`

```python
class pysched-lightning.task(scheduler, trigger, interval, priority)
```

`trigger` must be `'cron'` or `'recur'`.

* Use `@task` decorator to define your function, then enqueue it:

  ```python
  @task(scheduler, trigger, interval, priority)
  def fn(args, kwargs):
      pass
    
  fn.delay(*args, **kwargs)
  ```

  `fn.delay(*args, **kwargs)`  is equivaluent to `sheduler.delay(trigger, interval, priority, fn, args, kwargs)` using normal function definition.



## Related Projects

* [Lib/sched.py](https://github.com/python/cpython/blob/3.7/Lib/sched.py) ([`sched` - Event scheduler](https://docs.python.org/3.7/library/sched.html))
* [APScheduler](https://github.com/agronholm/apscheduler) ([apscheduler.readthedocs.org](http://apscheduler.readthedocs.org))

