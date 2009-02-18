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
Miscellaneous utilities for :mod:`repoze.what` when used in a Pylons
application.

"""

from pylons import request

from repoze.what.predicates import Predicate


__all__ = ['booleanize_predicates', 'debooleanize_predicates']


#{ Booleanizers


def booleanize_predicates():
    """
    Make :mod:`repoze.what` predicates evaluable without passing the 
    ``environ`` explicitly.
    
    """
    Predicate.__nonzero__ = lambda self: self.is_met(request.environ)


def debooleanize_predicates():
    """
    Stop :mod:`repoze.what` predicates from being evaluable without passing the 
    ``environ`` explicitly.
    
    This function reverts :func:`booleanize_predicates`.
    
    """
    del Predicate.__nonzero__


#}
