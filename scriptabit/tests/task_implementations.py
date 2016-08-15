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
from copy import deepcopy
from pkg_resources import resource_filename

from scriptabit import (
    Task,
    Difficulty,
    CharacterAttribute,
    SyncStatus,
    TaskService,
    TaskMap)


class TestTask(Task):

    @staticmethod
    def create_from(src):
        t = TestTask(id=uuid.uuid4())
        return t._copy_fields(src)

class TestTaskService(TaskService):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.persisted_tasks = []

    def get_all_tasks(self):
        """ Get all tasks """
        return self.tasks

    def persist_tasks(self, tasks):
        self.persisted_tasks = tasks

    def create(self, src):
        t = TestTask.create_from(src)
        t.status = SyncStatus.new
        return t
