
from redengine.core.task import base
from redengine.core.condition import Statement, Historical, Comparable
from redengine.core.time import TimeDelta
from .time import IsPeriod
from redengine.time.construct import get_before, get_between, get_full_cycle ,get_after

import os, re
import datetime
import numpy as np

# TODO: instead of "Statement.session.get_task", use self.session

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' stared {period}")
class TaskStarted(Historical, Comparable):

    """Condition for whether a task has started
    (for given period).

    Examples
    --------

    **Parsing example:**

    >>> from redengine.parse import parse_condition
    >>> parse_condition("'mytask' started")
    TaskStarted(task='mytask')
    """

    __parsers__ = {
        re.compile(r"'(?P<task>.+)' started"): "__init__",
    }

    def observe(self, task, _start_=None, _end_=None, **kwargs):

        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right

        records = task.logger.get_records(timestamp=(_start_, _end_), action="run")
        run_times = [record["timestamp"] for record in records]
        return run_times
        
    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        period = self.period
        task = self.kwargs["task"]
        return f"task '{task}' started {period}"

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' failed {period}")
class TaskFailed(Historical, Comparable):

    def observe(self, task, _start_=None, _end_=None, **kwargs):
        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            # If no period, start and end are the ones from the task
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right
        
        records = task.logger.get_records(timestamp=(_start_, _end_), action="fail")
        return [record["timestamp"] for record in records]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        period = self.period
        task = self.kwargs["task"]
        return f"task '{task}' failed {period}"

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' terminated {period}")
class TaskTerminated(Historical, Comparable):

    def observe(self, task, _start_=None, _end_=None, **kwargs):

        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            # If no period, start and end are the ones from the task
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right
        
        records = task.logger.get_records(timestamp=(_start_, _end_), action="terminate")
        return [record["timestamp"] for record in records]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        period = self.period
        task = self.kwargs["task"]
        return f"task '{task}' terminated {period}"

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' succeeded {period}")
class TaskSucceeded(Historical, Comparable):

    def observe(self, task, _start_=None, _end_=None, **kwargs):

        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right
        
        records = task.logger.get_records(timestamp=(_start_, _end_), action="success")
        return [record["timestamp"] for record in records]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        period = self.period
        task = self.kwargs["task"]
        return f"task 'task '{task}' succeeded {period}"

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' finished {period}")
class TaskFinished(Historical, Comparable):

    def observe(self, task, _start_=None, _end_=None, **kwargs):

        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right

        records = task.logger.get_records(timestamp=(_start_, _end_), action=["success", "fail", "terminate"])
        return [record["timestamp"] for record in records]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        period = self.period
        task = self.kwargs["task"]
        return f"task '{task}' finished {period}"

#@Statement.from_func(historical=False, quantitative=False, str_repr="task '{task}' is running")
class TaskRunning(Historical):

    __parsers__ = {
        re.compile(r"while '(?P<task>.+)' is running"): "__init__",
        re.compile(r"'(?P<task>.+)' is running"): "__init__",
    }

    def observe(self, task, **kwargs):

        task = Statement.session.get_task(task)

        record = task.logger.get_latest()
        if not record:
            return False
        return record["action"] == "run"

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        return f"task '{task}' is running"

#@Statement.from_func(historical=True, quantitative=True, str_repr="task '{task}' inacted")
class TaskInacted(Historical, Comparable):
    def observe(self, task, _start_=None, _end_=None, **kwargs):

        task = Statement.session.get_task(task)
        if _start_ is None and _end_ is None:
            # If no period, start and end are the ones from the task
            now = datetime.datetime.now()
            interv = task.period.rollback(now)
            _start_, _end_ = interv.left, interv.right
        
        records = task.logger.get_records(timestamp=(_start_, _end_), action="inaction")
        return [record["timestamp"] for record in records]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        return f"task '{task}' inacted"

class TaskExecutable(Historical):
    """Condition for checking whether a given
    task has not finished (for given period).

    Examples
    --------

    **Parsing example:**

    >>> from redengine.parse import parse_condition
    >>> parse_condition("daily between 10:00 and 15:00")
    TaskExecutable(task=None, period=TimeOfDay('10:00', '15:00'))

    """

    def __init__(self, retries=None, task=None, period=None, **kwargs):
        if retries is not None:
            kwargs["retries"] = retries
        super().__init__(period=period, task=task, **kwargs)

        # TODO: If constant launching (allow launching alive tasks)
        # is to be implemented, there should be one more condition:
        # self._is_not_running

        # TODO: How to consider termination? Probably should be considered as failures without retries
        # NOTE: inaction is not considered at all

    def __bool__(self):
        period = self.period
        retries = self.kwargs.get("retries", 0)
        task = self.kwargs["task"]

        # Form the sub statements
        has_not_succeeded = TaskSucceeded(period=period, task=task) == 0
        has_not_inacted = TaskInacted(period=period, task=task) == 0
        has_not_failed = TaskFailed(period=period, task=task) <= retries
        has_not_terminated = TaskTerminated(period=period, task=task) == 0

        isin_period = (
            # TimeDelta has no __contains__. One cannot say whether now is "past 2 hours".
            #   And please tell why this does not raise an exception then? - Future me
            True  
            if isinstance(period, TimeDelta) 
            else IsPeriod(period=period)
        )

        return (
            bool(isin_period)
            and bool(has_not_inacted)
            and bool(has_not_succeeded)
            and bool(has_not_failed)
            and bool(has_not_terminated)
        )

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        period = self.period
        return f"task '{task}' {self.period} "

    @classmethod
    def _from_period(cls, span_type=None, **kwargs):
        period_func = {
            "between": get_between,
            "after": get_after,
            "before": get_before,
            "starting": get_full_cycle,
            None: get_full_cycle,
            "every": TimeDelta,
        }[span_type]
        period = period_func(**kwargs)
        return cls(period=period)

    __parsers__ = {
        re.compile(r"(run )?(?P<type_>monthly|weekly|daily|hourly|minutely) (?P<span_type>starting) (?P<start>.+)"): "_from_period",
        re.compile(r"(run )?(?P<type_>monthly|weekly|daily|hourly|minutely) (?P<span_type>between) (?P<start>.+) and (?P<end>.+)"): "_from_period",
        re.compile(r"(run )?(?P<type_>monthly|weekly|daily|hourly|minutely) (?P<span_type>after) (?P<start>.+)"): "_from_period",
        re.compile(r"(run )?(?P<type_>monthly|weekly|daily|hourly|minutely) (?P<span_type>before) (?P<end>.+)"): "_from_period",
        re.compile(r"(run )?(?P<type_>monthly|weekly|daily|hourly|minutely)"): "_from_period",
        re.compile(r"(run )?(?P<span_type>every) (?P<past>.+)"): "_from_period",
    }

#@Statement.from_func(historical=False, quantitative=False, str_repr="task '{depend_task}' finished before {task} started")
class DependFinish(Historical):
    """Condition for checking whether a given
    task has not finished after running a dependent 
    task.

    Examples
    --------

    **Parsing example:**

    >>> from redengine.parse import parse_condition
    >>> parse_condition("after 'other' finished")
    DependFinish(task=None, depend_task='other')
    """
    __parsers__ = {
        re.compile(r"after '(?P<depend_task>.+)' finished"): "__init__",
    }
    def __init__(self, depend_task, task=None, **kwargs):
        super().__init__(task=task, depend_task=depend_task, **kwargs)

    def observe(self, task, depend_task, **kwargs):
        """True when the "depend_task" has finished and "task" has not yet ran after it.
        Useful for start cond for task that should be run after finish of another task.
        """
        # Name ideas: TaskNotRanAfterFinish, NotRanAfterFinish, DependFinish
        # HasRunAfterTaskFinished, RanAfterTask, RanAfterTaskFinished, AfterTaskFinished
        # TaskRanAfterFinish
        actual_task = Statement.session.get_task(task)
        depend_task = Statement.session.get_task(depend_task)

        last_depend_finish = depend_task.logger.get_latest(action=["success", "fail"])
        last_actual_start = actual_task.logger.get_latest(action=["run"])

        if not last_depend_finish:
            # Depend has not run at all
            return False
        elif not last_actual_start:
            # Depend has finished but the actual task has not
            return True

        return last_depend_finish["created"] > last_actual_start["created"]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        depend_task = self.kwargs["depend_task"]
        return f"task '{depend_task}' finished before {task} started"


#@Statement.from_func(historical=False, quantitative=False, str_repr="task '{depend_task}' succeeded before {task} started")
class DependSuccess(Historical):
    """Condition for checking whether a given
    task has not succeeded after running a dependent 
    task.

    Examples
    --------

    **Parsing example:**

    >>> from redengine.parse import parse_condition
    >>> parse_condition("after 'other' succeeded")
    DependSuccess(task=None, depend_task='other')

    """

    __parsers__ = {
        re.compile(r"after '(?P<depend_task>.+)'( succeeded)?"): "__init__",
    }

    def __init__(self, depend_task, task=None, **kwargs):
        super().__init__(task=task, depend_task=depend_task, **kwargs)

    def observe(self, task, depend_task, **kwargs):
        """True when the "depend_task" has succeeded and "task" has not yet ran after it.
        Useful for start cond for task that should be run after success of another task.
        """
        actual_task = Statement.session.get_task(task)
        depend_task = Statement.session.get_task(depend_task)

        last_depend_finish = depend_task.logger.get_latest(action=["success"])
        last_actual_start = actual_task.logger.get_latest(action=["run"])

        if not last_depend_finish:
            # Depend has not run at all
            return False
        elif not last_actual_start:
            # Depend has succeeded but the actual task has not
            return True
            
        return last_depend_finish["timestamp"] > last_actual_start["timestamp"]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        depend_task = self.kwargs["depend_task"]
        return f"task '{depend_task}' finished before {task} started"

#@Statement.from_func(historical=False, quantitative=False, str_repr="task '{depend_task}' failed before {task} started")
class DependFailure(Historical):
    """Condition for checking whether a given
    task has not failed after running a dependent 
    task.

    Examples
    --------

    **Parsing example:**

    >>> from redengine.parse import parse_condition
    >>> parse_condition("after 'other' failed")
    DependFailure(task=None, depend_task='other')
    """

    __parsers__ = {
        re.compile(r"after '(?P<depend_task>.+)' failed"): "__init__",
    }

    def __init__(self, depend_task, task=None, **kwargs):
        super().__init__(task=task, depend_task=depend_task, **kwargs)

    def observe(self, task, depend_task, **kwargs):
        """True when the "depend_task" has failed and "task" has not yet ran after it.
        Useful for start cond for task that should be run after failure of another task.
        """
        actual_task = Statement.session.get_task(task)
        depend_task = Statement.session.get_task(depend_task)

        last_depend_finish = depend_task.logger.get_latest(action=["fail"])
        last_actual_start = actual_task.logger.get_latest(action=["run"])

        if not last_depend_finish:
            # Depend has not run at all
            return False
        elif not last_actual_start:
            # Depend has failed but the actual task has not
            return True
            
        return last_depend_finish["timestamp"] > last_actual_start["timestamp"]

    def __str__(self):
        if hasattr(self, "_str"):
            return self._str
        task = self.kwargs["task"]
        depend_task = self.kwargs["depend_task"]
        return f"task '{depend_task}' finished before {task} started"