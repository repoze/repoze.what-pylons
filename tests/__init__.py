# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009, Gustavo Narea <me@gustavonarea.net>.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Test suite for the repoze.what Pylons plugin.

This module includes miscellaneous tests.

"""

from inspect import ismethod
from unittest import TestCase

from repoze.what.plugins.pylonshq import ControllerProtector


class TestControllerDecorator(TestCase):
    """Test case for @ControllerProtector decorator with a handler"""
    
    def test__before__is_defined_as_instance_method(self):
        """The ``__before__`` method must be defined as an instance method"""
        # Creating a fake decorated controller
        class DaController(object): pass
        DaController = ControllerProtector(None)(DaController)
        # Testing it:
        assert hasattr(DaController, '__before__')
        assert ismethod(DaController.__before__)
