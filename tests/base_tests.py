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
Tests for this plugin when used in TurboGears 2.

"""

import os, shutil

from unittest import TestCase

import pylons
from pylons import tmpl_context
from pylons.util import ContextObj, PylonsContext

from tests.base_app import make_app, session_dir

# Just in case...
shutil.rmtree(session_dir, ignore_errors=True)


class TestWSGIController(TestCase):

    def setUp(self):
        # Creating the session dir:
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        # Setting Pylons up:
        c = ContextObj()
        py_obj = PylonsContext()
        py_obj.c = c
        py_obj.request = py_obj.response = None
        self.environ = {
            'pylons.routes_dict': dict(action='index'),
            'paste.config': dict(global_conf=dict(debug=True)),
            'pylons.pylons': py_obj,
            #'repoze.who.identity': {}
            }
        pylons.c._push_object(c)
        # Finally, the app:
        self.app = make_app(self.controller, self.environ)

    def tearDown(self):
        tmpl_context._pop_object()
        # Removing the session dir:
        shutil.rmtree(session_dir, ignore_errors=True)
    
    def make_environ(self, userid):
        environ = {
            'repoze.who.identity': {'repoze.who.userid': userid}
            }
        return environ


class ActionDecoratorTestCase(object):
    """Test case for @ActionProtector decorator"""
    
    def test_authorization_granted_to_anonymous_user(self):
        resp = self.app.get('/', status=200)
        assert 'hello world' in resp.body, resp.body
    
    def test_authorization_denied_to_anonymous_user(self):
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'admin'
        resp = self.app.get('/admin', status=302)
        expected_location = 'http://localhost/login?came_from=' \
                            'http%3A%2F%2Flocalhost%2Fadmin'
        assert resp.location == expected_location
    
    def test_authorization_granted_to_authenticated_user(self):
        resp = self.app.get('/login_handler?login=rms&password=freedom')
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'admin'
        resp = self.app.get('/admin')
        assert 'got to admin' in resp.body, resp.body
        
    def test_authorization_denied_to_authenticated_user(self):
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'admin'
        environ = self.make_environ('linus')
        self.app.get('/admin', extra_environ=environ, status=403)
        
    def test_authorization_denied_with_custom_denial_handler(self):
        resp = self.app.get('/login_handler?login=sballmer&password=developers')
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'leave_comment'
        resp = self.app.get('/leave_comment', status=403)
        assert 'Trolls are banned' in resp.body, resp.body
        
    def test_authorization_denied_with_default_denial_handler(self):
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'logout'
        resp = self.app.get('/logout', status=200)
        assert 'why make a try then?' in resp.body, resp.body
        
    def test_authorization_denied_with_default_denial_handler_overriden(self):
        resp = self.app.get('/login_handler?login=sballmer&password=developers')
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'start_thread'
        resp = self.app.get('/start_thread', status=403)
        assert 'Trolls are banned' in resp.body, resp.body
        
    def test_action_signature_is_not_changed(self):
        """@ActionProtector must not change the signature of the action"""
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'get_parameter'
        self.environ['pylons.routes_dict']['something'] = 'foo'
        resp = self.app.get('/get_parameter/foo', status=200)
        assert 'Parameter received: foo' in resp.body, resp.body


class ControllerDecoratorTestCase(object):
    """Test case for @ControllerProtector decorator"""
    
    def test_controller_wide_authorization_granted(self):
        resp = self.app.get('/login_handler?login=rms&password=freedom')
        resp = self.app.get('/', status=200)
        assert 'you are in the panel' in resp.body, resp.body
    
    def test_controller_wide_authorization_denied(self):
        # A little hack for Pylons; not required in TG2:
        self.environ['pylons.routes_dict']['action'] = 'commit'
        resp = self.app.get('/commit', status=302)


class ControllerDecoratorWithHandlerTestCase(object):
    """Test case for @ControllerProtector decorator with a handler"""
    
    def test_controller_wide_authorization_denied(self):
        resp = self.app.get('/', status=200)
        assert 'you are in the panel with handler' in resp.body, resp.body
