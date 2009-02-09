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
Decorators to control access to controllers and controller actions in a
Pylons or TurboGears 2 application.

All these utilities are also available in the 
:mod:`repoze.what.plugins.pylonshq` namespace.

"""

from pylons import request, response
from pylons.controllers.util import abort
from repoze.what.predicates import NotAuthorizedError

__all__ = ['ActionProtector', 'ControllerProtector']


class _BaseProtectionDecorator(object):
    
    default_denial_handler = None
    
    def __init__(self, predicate, denial_handler=None):
        """
        Make :mod:`repoze.what` verify that the predicate is met.
        
        :param predicate: A :mod:`repoze.what` predicate.
        :param denial_handler: The callable to be run if authorization is
            denied (overrides :attr:`default_denial_handler` if defined).
        
        If called, ``denial_handler`` will be passed a positional argument 
        which represents a message on why authorization was denied.
        
        """
        self.predicate = predicate
        self.denial_handler = denial_handler or self.default_denial_handler


class ActionProtector(_BaseProtectionDecorator):
    """
    Function decorator to set predicate checkers in Pylons/TG2 controller
    actions.
    
    When authorization is denied, :func:`pylons.controllers.util.abort` will
    be called with the 401 or 403 HTTP status code if the current user is
    anonymous or authenticated, respectively.
    
    It's worth noting that when the status code for the response is 401,
    that will trigger a :mod:`repoze.who` challenger (e.g., a login form will
    be displayed).
    
    .. attribute:: default_denial_handler = None
    
        :type: callable
        
        The default denial handler.
    
    """
    
    def __call__(self, func):
        """
        Return the decorator that will verify authorization when ``func`` is
        run.
        
        """
        
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


class ControllerProtector(_BaseProtectionDecorator):
    """
    Class decorator to set predicate checkers in Pylons/TG2 controllers.
    
    .. attribute:: default_denial_handler = None
    
        :type: callable or str
        
        The default denial handler to be passed to :attr:`protector`.
        
        When it's set as a string, the resulting handler will be the attribute
        of the controller class whose name is represented by
        ``default_denial_handler``. For example, if ``default_denial_handler``
        equals ``"process_errors"`` and the decorated controller is
        ``NiceController``, the resulting denial handler will be:
        ``NiceController.process_errors``.
    
    .. attribute:: protector = ActionProtector
    
        :type: Subclass of :class:`ActionProtector`
        
        The action protection decorator to be added to 
        ``Controller.__before__``.
    
    
    """
    
    protector = ActionProtector
    
    def __call__(self, cls):
        """
        Add the :attr:`protector` decorator to the ``__before__`` method of the
        ``cls`` controller class.
        
        """
        
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
