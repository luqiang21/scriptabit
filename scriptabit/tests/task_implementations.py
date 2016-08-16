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
    def __init__(
            self,
            _id,
            name='',
            description='',
            completed=False,
            difficulty=Difficulty.easy,
            attribute=CharacterAttribute.strength,
            status=SyncStatus.new):
        super().__init__(_id, name, description, completed, difficulty,
                         attribute, status)

    @property
    def name(self):
        """ Task name """
        return self.__name

    @name.setter
    def name(self, name):
        """ Task name """
        self.__name = name

    @property
    def description(self):
        """ Task description """
        return self.__description

    @description.setter
    def description(self, description):
        """ Task description """
        self.__description = description

    @property
    def completed(self):
        """ Task completed """
        return self.__completed

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        self.__completed = completed

    @property
    def difficulty(self):
        """ Task difficulty """
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        self.__difficulty = difficulty

    @property
    def attribute(self):
        """ Task character attribute """
        return self.__attribute

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        if not isinstance(attribute, CharacterAttribute):
            raise TypeError
        self.__attribute = attribute

    @property
    def status(self):
        """ Task status """
        return self.__status

    @status.setter
    def status(self, status):
        """ Task status """
        self.__status = status


class TestTaskService(TaskService):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.persisted_tasks = []

    def get_all_tasks(self):
        """ Get all tasks """
        return self.tasks

    def get_task(self, _id):
        """ Gets a task by id """
        # Quick and nasty sequential search, good enough for testing
        for t in self.tasks:
            if t.id == _id:
                return t
        return None

    def persist_tasks(self, tasks):
        self.persisted_tasks = tasks

    def _create_task(self):
        return TestTask(_id=uuid.uuid4())
