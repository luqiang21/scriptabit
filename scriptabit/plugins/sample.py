# -*- coding: utf-8 -*-
""" A sample plugin.
Doesn't do anything, but it makes a good template for new plugins.
Unused methods can be deleted.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

import scriptabit

class Sample(scriptabit.IPlugin):
    """ Scriptabit sample plugin.
    """

    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Note that to avoid argument name conflicts, only long argument names
        should be used, and they should be prefixed with the plugin-name or
        unique abbreviation.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        # parser.add(
            # '--sample-plugin-argument',
            # required=False,
            # default=20.0,
            # type=float,
            # help='Sample plugin value')

        return parser

    def activate(self):
        """ Called by the plugin framework when a plugin is activated."""
        pass

    def deactivate(self):
        """ Called by the plugin framework when a plugin is deactivated."""
        pass

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Generally, any initialisation should be done here rather than in
        activate or __init__.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """
        super().initialise(configuration, habitica_service)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        return 60

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        logging.getLogger(__name__).info('Sample plugin doing stuff ...')

        # do work here

        # return False if finished, and True to be updated again.
        return False