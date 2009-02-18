***********************
Miscellaneous utilities
***********************

.. topic:: Overview

    This plugin provides miscellaneous utilities to make using 
    :mod:`repoze.what` easier.


Boolean predicates
==================

:mod:`repoze.what` predicates can't be evaluated unless you pass the WSGI
environment dictionary, whenever you want to evaluate them. Nevertheless,
this plugin enables you to evaluate predicate checker instances as boolean
values without passing the ``environ``.

This function is :func:`repoze.what.plugins.pylonshq.booleanize_predicates` and
you have to call it once, then you'll be able to evaluate your predicates
without passing the environ::

    >>> from repoze.what.predicates import not_anonymous
    >>> p = non_anonymous()
    >>> bool(p) # Will return False if the user is anonymous; True otherwise
    False

instead of::

    >>> from pylons import request
    >>> from repoze.what.predicates import not_anonymous
    >>> p = non_anonymous()
    >>> p.is_met(request.environ) # Will return False if the user is anonymous; True otherwise
    False

Keep in mind that you don't have to call this function multiple times -- once 
is enough. For example, you could call it in the function where you set up the
application in ``{pylonsproject}.config.middleware``::

    # (...)
    from repoze.what.plugins.pylonshq import booleanize_predicates
    # (...)
    
    def make_app(global_conf, full_stack=True, **app_conf):
        # (...)
        booleanize_predicates()
        # (...)
        return app

.. tip::
    If you ever need to disable this "magical" behavior, you should use
    :func:`repoze.what.plugins.pylonshq.debooleanize_predicates`.

.. note::
    **TurboGears 2 users:** TG calls this function for you, unless you disabled
    the default auth mechanism in ``{tg2application}.config.app_cfg``.
