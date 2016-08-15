# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
import json
import pytest
import requests
import requests_mock
import uuid

from pkg_resources import resource_filename
from random import randint, choice

from bidict import (
    KeyDuplicationError,
    ValueDuplicationError,
    KeyAndValueDuplicationError)
from tempfile import NamedTemporaryFile
from scriptabit import (
    SyncStatus,
    TaskSync,
    Task,
    TaskMap,
    Difficulty,
    CharacterAttribute)

from .task_implementations import TestTaskService, TestTask


difficulties = (
    Difficulty.trivial,
    Difficulty.easy,
    Difficulty.medium,
    Difficulty.hard)

attributes = (
    CharacterAttribute.strength,
    CharacterAttribute.intelligence,
    CharacterAttribute.constitution,
    CharacterAttribute.perception)

def random_task():
    t = TestTask(id=uuid.uuid4())
    t.name = uuid.uuid1()
    t.description = 'blah blah tired blah coffee'
    t.completed = choice((True, False))
    t.difficulty = difficulties[randint(0,len(difficulties)-1)]
    t.attribute = attributes[randint(0,len(attributes)-1)]
    t.status = SyncStatus.unchanged
    return t

def test_new_tasks():
    src_tasks = [random_task() for x in range(3)]
    dst_tasks = []
    src = TestTaskService(src_tasks)
    dst = TestTaskService(dst_tasks)
    map = TaskMap()
    sync = TaskSync(src, dst, map)
    sync.synchronise()

    assert len(dst.persisted_tasks) == len(src_tasks)
    for d in dst.persisted_tasks:
        assert d.status == SyncStatus.new
        assert d in dst_tasks
        assert map.try_get_src_id(d)

    for s in src.get_all_tasks():
        dst_id = map.try_get_dst_id(s)
        assert dst_id
        d = dst.get_task(dst_id)
        assert s.name == d.name
        assert s.description == d.description
        assert s.completed == d.completed
        assert s.difficulty == d.difficulty
        assert s.attribute == d.attribute

def test_existing_tasks_are_updated():
    src = random_task()
    src_tasks = [src]
    src_svc = TestTaskService(src_tasks)
    dst = random_task()
    dst.description = 'something different'
    dst_tasks = [dst]
    dst_svc = TestTaskService(dst_tasks)

    # precondition tests
    assert src.id != dst.id
    assert src.status == SyncStatus.unchanged
    assert dst.name != src.name
    assert dst.attribute != src.attribute
    assert dst.difficulty != src.difficulty
    assert dst.status == SyncStatus.unchanged
    assert dst.description != src.description
    map = TaskMap()
    map.map(src, dst)

    sync = TaskSync(src_svc, dst_svc, map)
    sync.synchronise()

    assert len(dst_svc.persisted_tasks) == 1
    actual = dst_svc.persisted_tasks[0]
    assert actual.id == dst.id, "id not changed"
    assert actual.id != src.id, "id not changed"
    assert actual.name == src.name
    assert actual.attribute == src.attribute
    assert actual.difficulty == src.difficulty
    assert actual.completed == src.completed
    assert actual.status == SyncStatus.updated
    assert actual.description == src.description
