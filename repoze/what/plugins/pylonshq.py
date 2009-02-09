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
Utilities to use :mod:`repoze.what` v1 in a Pylons or TurboGears 2 application.

"""

from pylons import request, response
from pylons.controllers.util import abort
from repoze.what.predicates import NotAuthorizedError

__all__ = ['ActionProtectionDecorator', 'ControllerProtectionDecorator']


class _BaseProtectionDecorator(object):
    
    defaul_denial_handler = None
    
    def __init__(self, predicate, denial_handler=None):
        """
        Make :mod:`repoze.what` verify that the predicate is met.
        
        :param action: The controller action to be protected.
        :param predicate: A :mod:`repoze.what` predicate.
        :param denial_handler: The callable to be run if authorization is
            denied.
        :raise HTTPUnauthorized: If authorization is denied and the current 
            user is anonymous (HTTP status code 401).
        :raise HTTPForbidden: If authorization is denied and the current user 
            is authenticated (HTTP status code 403).
        :return: The decorator that checks authorization.
        
        If called, ``denial_handler`` will be passed a positional argument which
        represents a message on why authorization was denied.
        
        """
        self.predicate = predicate
        self.denial_handler = denial_handler or self.defaul_denial_handler


class ActionProtectionDecorator(_BaseProtectionDecorator):
    """
    Decorator to set predicate checkers in Pylons/TG2 controller actions.
    
    """
    
    def __call__(self, func):
        
        def check(*args, **kwargs):
            try:
                self.predicate.check_authorization(request.environ)
            except NotAuthorizedError, e:
                reason = unicode(e)
                if request.environ.get('repoze.who.identity'):
                    # The user is authenticated.
                    code = 403
                else:
                    # The user is not authenticated.
                    code = 401
                if self.denial_handler:
                    response.status = code
                    return self.denial_handler(reason)
                abort(code, comment=reason)
            return func(*args, **kwargs)
        
        return check


class ControllerProtectionDecorator(_BaseProtectionDecorator):
    """
    Decorator to set predicate checkers in Pylons/TG2 controllers.
    
    """
    
    protector = ActionProtectionDecorator
    
    def __call__(self, cls):
        if callable(self.denial_handler) or self.denial_handler is None:
            denial_handler = self.denial_handler
        else:
            denial_handler = getattr(cls, self.denial_handler)
        if hasattr(cls, '__before__'):
            old_before = cls.__before__
        else:
            def old_before(*args, **kwargs): pass
        protector = self.protector(self.predicate, denial_handler)
        cls.__before__ = protector(old_before)
        
        return cls
