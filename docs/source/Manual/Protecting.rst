*********************************************
Protecting controllers and controller actions
*********************************************

.. topic:: Overview

    This plugin provides decorators to add access rules to controllers and
    controller actions, which have been created with extensibility in mind
    so that you can adapt them to suit your needs.


Protecting a controller action
==============================

To set controller-wide access rules, you can use the
:class:`ActionProtector <repoze.what.plugins.pylonshq.ActionProtector>`
class decorator as in the example below::

    from repoze.what.predicates import has_permission
    from repoze.what.plugins.pylonshq import ActionProtector
    
    class RootController(YourBaseController):
        
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        @ActionProtector(has_permission('edit-articles'))
        def edit_article(self, article_id):
            return get_article_edition_form(article_id)


With the controller and action controllers above, anyone who tries to access
``/edit_article`` will have to be granted the ``edit-articles`` permission.
Otherwise, authorization will be denied.

.. tip::

    TurboGears 2 provides the :class:`tg.require` decorator to set
    the access rules in controller actions, which is a subclass of
    :class:`ActionProtector <repoze.what.plugins.pylonshq.ActionProtector>`
    with additional functionality specific to TG2 applications.


Protecting a controller
=======================

To set controller-wide access rules, you can use the
:class:`ControllerProtector <repoze.what.plugins.pylonshq.ControllerProtector>`
class decorator as in the example below::

    from repoze.what.predicates import has_permission
    from repoze.what.plugins.pylonshq import ControllerProtector
    
    @ControllerProtector(has_permission('manage'))
    class ControlPanel(YourBaseController):
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        def delete_user(self, user_id):
            return nice_function_to_delete_a_user(user_id)
    
    class RootController(YourBaseController):
        
        panel = ControlPanel()
        
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()


With the controllers and action controllers above, anyone who tries to access
``/panel/*`` will have to be granted the ``manage`` permission. Otherwise, 
authorization will be denied.

.. tip::

    As of version 2.0b6, TurboGears provides the :class:`tg.allow_only` 
    decorator for controller-wide authorization, which is a subclass of
    :class:`ControllerProtector <repoze.what.plugins.pylonshq.ControllerProtector>`
    with additional functionality specific to TG2 applications.

.. note::

    If you're using Python v2.4 or v2.5, you will have to use the alternate
    syntax because class decorators are supported as of Python v2.6::

        class ControlPanel(YourBaseController):
            # ...
            pass
        ControlPanel = ControllerProtector(has_permission('manage'))(ControlPanel)


Using denial handlers
=====================

By default, an authorization denial triggers one of the following actions:

* If the user is anonymous, :mod:`repoze.who` will perform a challenge (e.g.,
  a login form will be displayed).
* If the user is authenticated, a page whose HTTP status code is 403 will be
  served.

If you want to override the default behavior when authorization is denied, you
have define a so-called "denial handler". A denial handler is a callable which
receives one positional argument (which is the message that describes why
authorization is denied; this is, the relevant :mod:`repoze.what` predicate
message) and is called only when authorization is denied.

The following is a denial handler::

    # This is yourapplication.anotherpackage
    
    from pylons import request, response
    # nice_flash is a function that inserts a user-visible message in the
    # template
    from yourapplication.somepackage import nice_flash
    
    def cool_denial_handler(reason):
        # When this handler is called, response.status has two possible values:
        # 401 or 403.
        if response.status.startswith('401'):
            message = 'Oops, you have to login: %s' % reason
            message_type = 'warning'
        else:
            identity = request.environ['repoze.who.identity']
            userid = identity['repoze.who.userid']
            message = "Come on, %s, you know you can't do that: %s" % (userid,
                                                                       reason)
            message_type = 'error'
        nice_flash(message, message_type)

And you can use it as in::

    from repoze.what.predicates import has_permission
    from repoze.what.plugins.pylonshq import ActionProtector, ControllerProtector
    
    from yourapplication.anotherpackage import cool_denial_handler
    
    @ControllerProtector(has_permission('manage'), cool_denial_handler)
    class ControlPanel(YourBaseController):
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        def delete_user(self, user_id):
            return nice_function_to_delete_a_user(user_id)
    
    class RootController(YourBaseController):
        
        panel = ControlPanel()
        
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        @ActionProtector(has_permission('edit-articles'), cool_denial_handler)
        def edit_article(self, article_id):
            return get_article_edition_form(article_id)

Then, when authorization is denied:

* If the user is anonymous, she should be served a web page which contains a
  login form and a message that starts with "Oops, you have to login (...)".
  The status code of such a response is up to the :mod:`repoze.who` challenger.
* If the user is authenticated, she should be served a web page that contains
  a message that starts with "Come on, ``{{username}}``, you know (..)" and 
  whose HTTP status code is 403.


Creating application-specific protectors
========================================

Sometimes you may need to customize the controller and controller action
protectors in many places within your application (or in the whole 
application). All you have to do is subclass the relevant protector.

For example, if we use the ``cool_denial_handler`` function above very often,
then we should create controller and controller action protectors which use
that handler by default::

    # This is yourapplication.yetanotherpackage
    
    from repoze.what.plugins.pylonshq import ActionProtector, ControllerProtector
    from yourapplication.anotherpackage import cool_denial_handler
    
    class CoolActionProtector(ActionProtector):
        default_denial_handler = staticmethod(cool_denial_handler)
    
    class CoolControllerProtector(ControllerProtector):
        default_denial_handler = staticmethod(cool_denial_handler)

Then our controllers would look like this::

    from repoze.what.predicates import has_permission
    
    from yourapplication.yetanotherpackage import CoolActionProtector, \
                                                  CoolControllerProtector
    
    @CoolControllerProtector(has_permission('manage'))
    class ControlPanel(YourBaseController):
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        def delete_user(self, user_id):
            return nice_function_to_delete_a_user(user_id)
    
    class RootController(YourBaseController):
        
        panel = ControlPanel()
        
        # Place an expose() here if you use TG2
        def index(self):
            return nice_function_to_do_nothing()
        
        # Place an expose() here if you use TG2
        @CoolActionProtector(has_permission('edit-articles'))
        def edit_article(self, article_id):
            return get_article_edition_form(article_id)

And every time authorization is denied, the ``cool_denial_handler`` function
will be called.
