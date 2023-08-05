
from redengine.parse.condition import parse_condition
from redengine.conditions import (
    AlwaysTrue, AlwaysFalse, 
    All, Any, Not,

    TaskRunning, TaskStarted, 
    TaskFailed, TaskSucceeded, TaskFinished,
    DependFailure, DependSuccess, DependFinish,
    TaskExecutable,

    IsPeriod,

    IsEnv,
)

from redengine.time import (
    TimeDelta,

    TimeOfMinute,
    TimeOfHour,
    TimeOfDay,
    TimeOfWeek,
    TimeOfMonth
)

import pytest

cases_time = [
    pytest.param("hourly",  TaskExecutable(period=TimeOfHour(None, None)), id="hourly"),
    pytest.param("daily",   TaskExecutable(period=TimeOfDay(None, None)), id="daily"),
    pytest.param("weekly",  TaskExecutable(period=TimeOfWeek(None, None)), id="weekly"),
    #pytest.param("monthly",  TaskExecutable(period=TimeOfMonth(None, None)), id="monthly"),

    pytest.param("hourly starting 45:00",   TaskExecutable(period=TimeOfHour("45:00", "45:00")), id="hourly starting"),
    pytest.param("daily starting 10:00",    TaskExecutable(period=TimeOfDay("10:00", "10:00")),  id="daily starting"),
    pytest.param("weekly starting Tuesday", TaskExecutable(period=TimeOfWeek("Tue", "Tue")),     id="weekly starting"),
    #pytest.param("monthly starting 1.",  TaskExecutable(period=TimeOfMonth(1, 1)), id="monthly starting"),

    pytest.param("hourly between 45:00 and 50:00",       TaskExecutable(period=TimeOfHour("45:00", "50:00")), id="hourly between"),
    pytest.param("daily between 10:00 and 14:00",        TaskExecutable(period=TimeOfDay("10:00", "14:00")),  id="daily between"),
    pytest.param("weekly between Tuesday and Wednesday", TaskExecutable(period=TimeOfWeek("Tue", "Wed")),     id="weekly between"),
    #pytest.param("monthly between 1. and 15.",  TaskExecutable(period=TimeOfMonth(1, 5)), id="monthly between"),

    pytest.param("hourly after 45:00",   TaskExecutable(period=TimeOfHour("45:00", None)), id="hourly after"),
    pytest.param("daily after 10:00",    TaskExecutable(period=TimeOfDay("10:00", None)),  id="daily after"),
    pytest.param("weekly after Tuesday", TaskExecutable(period=TimeOfWeek("Tue", None)),   id="weekly after"),
    #pytest.param("monthly after 1.",  TaskExecutable(period=TimeOfMonth(1, None)), id="monthly after"),

    pytest.param("hourly before 45:00",   TaskExecutable(period=TimeOfHour(None, "45:00")), id="hourly before"),
    pytest.param("daily before 10:00",    TaskExecutable(period=TimeOfDay(None, "10:00")), id="daily before"),
    pytest.param("weekly before Tuesday", TaskExecutable(period=TimeOfWeek(None, "Tue")), id="weekly before"),
    #pytest.param("monthly before 1.",  TaskExecutable(period=TimeOfMonth(None, 1)), id="monthly before"),

    # Time delta
    pytest.param("every 1 hours", TaskExecutable(period=TimeDelta("1 hours")), id="every hour"),
    pytest.param("every 1 days 1 hours 30 minutes 30 seconds", TaskExecutable(period=TimeDelta("1 days 1 hours 30 minutes 30 seconds")), id="every hour 30 mins 30 seconds"),

    # IsTimeOf...
    pytest.param("time of hour between 45:00 and 50:00",       IsPeriod(period=TimeOfHour("45:00", "50:00")), id="time of hour between"),
    pytest.param("time of day between 10:00 and 14:00",        IsPeriod(period=TimeOfDay("10:00", "14:00")), id="time of day between"),
    pytest.param("time of week between Tuesday and Wednesday", IsPeriod(period=TimeOfWeek("Tue", "Wed")), id="time of week between"),
    #pytest.param("time of month between 1. and 15.",  IsPeriod(period=TimeOfMonth(1, 5)), id="time of month between"),

    pytest.param("time of hour after 45:00",   IsPeriod(period=TimeOfHour("45:00", None)), id="time of hour after"),
    pytest.param("time of day after 10:00",    IsPeriod(period=TimeOfDay("10:00", None)), id="time of day after"),
    pytest.param("time of week after Tuesday", IsPeriod(period=TimeOfWeek("Tue", None)), id="time of week after"),
    #pytest.param("time of month after 1.",  IsPeriod(period=TimeOfMonth(1, None)), id="time of month after"),

    pytest.param("time of hour before 45:00",   IsPeriod(period=TimeOfHour(None, "45:00")), id="time of hour before"),
    pytest.param("time of day before 10:00",    IsPeriod(period=TimeOfDay(None, "10:00")), id="time of day before"),
    pytest.param("time of week before Tuesday", IsPeriod(period=TimeOfWeek(None, "Tue")), id="time of week before"),
    #pytest.param("time of month before 1.",  IsPeriod(period=TimeOfMonth(None, 1)), id="time of month before"),
]

cases_task = [
    # Single task related
    pytest.param("while 'mytask' is running", TaskRunning(task="mytask"), id="while task running"),
    pytest.param("'mytask' started", TaskStarted(task="mytask"), id="after task started"),

    # Task dependent related (requires 2 tasks)
    pytest.param("after 'other'",           DependSuccess(depend_task="other"), id="after task"),
    pytest.param("after 'other' succeeded", DependSuccess(depend_task="other"), id="after task successs"),
    pytest.param("after 'other' failed",    DependFailure(depend_task="other"), id="after failed"),
    pytest.param("after 'other' finished",  DependFinish(depend_task="other"), id="after finished"),
    pytest.param("after 'group1.group-2.mytask+'", DependSuccess(depend_task="group1.group-2.mytask+"), id="after task special chars"),
]

cases_logical = [
    pytest.param("always true", AlwaysTrue(), id="AlwaysTrue"),
    pytest.param("always false", AlwaysFalse(), id="AlwaysTrue"),
    pytest.param("true", AlwaysTrue(), id="true"),
    pytest.param("false", AlwaysFalse(), id="false"),

    # Logical operations
    pytest.param("always true & always false", All(AlwaysTrue(), AlwaysFalse()), id="Logical AND"),
    pytest.param("always true | always false", Any(AlwaysTrue(), AlwaysFalse()), id="Logical OR"),
    pytest.param("~ always false", Not(AlwaysFalse()), id="Logical NOT"),
]

cases_misc = [
    pytest.param("env 'test'", IsEnv('test'), id="IsEnv 'test'"),
]


# All cases
cases = cases_logical + cases_task + cases_time + cases_misc

@pytest.mark.parametrize(
    "cond_str,expected", cases
)
def test_string(cond_str, expected):
    cond = parse_condition(cond_str)
    assert cond == expected

@pytest.mark.parametrize(
    "cond_str,expected", cases
)
def test_back_to_string(cond_str, expected):
    cond = parse_condition(cond_str)
    cond_as_str = str(cond)
    cond_2 = parse_condition(cond_as_str)
    assert cond == cond_2
    #assert cond_str == cond_as_str