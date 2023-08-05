

from redengine.conditions import (
    IsEnv
)
from redengine.core.condition import Statement, Comparable, Historical

import pytest


def test_env(session):
    
    cond = IsEnv("test")
    assert not bool(cond)

    session.env = "test"
    assert bool(cond)

    session.env = "prod"
    assert not bool(cond)
