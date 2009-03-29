***********************
Miscellaneous utilities
***********************

Because :mod:`repoze.what` is framework-independent, its predicates can only
be evaluated if you pass the WSGI environ whenever you want to evaluate them.
But to makes things easier, this plugin defines utilities to evaluate
predicates without passing the environ explicitly:


Predicate evaluators
====================

With :func:`repoze.what.plugins.pylonshq.is_met`, you'll be able to evaluate
your predicates without passing the WSGI environ explicitly, as in:

    >>> from repoze.what.plugins.pylonshq import is_met
    >>> from repoze.what.predicates import is_user
    >>> is_met(is_user('gustavo')) # Will return True if the user is "gustavo"
    False

instead of:

    >>> from pylons import request
    >>> from repoze.what.predicates import is_user
    >>> p = is_user('gustavo')
    >>> p.is_met(request.environ) # Will return True if the user is "gustavo"
    False

If you want to evaluate the opposite, that it's not met, you can use
:func:`not_met <repoze.what.plugins.pylonshq.not_met>` instead:

    >>> from repoze.what.plugins.pylonshq import not_met
    >>> from repoze.what.predicates import is_user
    >>> not_met(is_user('gustavo')) # Will return True if the user isn't "gustavo"
    True

instead of:

    >>> from pylons import request
    >>> from repoze.what.predicates import is_user
    >>> p = is_user('gustavo')
    >>> not p.is_met(request.environ) # Will return True if the user isn't "gustavo"
    True


Boolean predicates
==================

.. warning::

    This functionality was implemented by popular demand, but it's **strongly
    discouraged** by the author of :mod:`repoze.what` because it's a
    monkey-patch which brings serious side-effects when enabled:
    
    1. Third-party components which handle :mod:`repoze.what` predicates may
       get erroneous values after evaluating a predicate checker (even if they
       don't use this functionality!).
    2. If another non-Pylons-based application uses the same monkey-patch and
       you mount it on your application (or vice versa), the predicates used
       by both application will share the same WSGI environ.
    
    In the two scenarios above, **it will lead to serious security flaws**. So
    *avoid it by all means!* Use `predicate evaluators`_ instead.

:func:`repoze.what.plugins.pylonshq.booleanize_predicates` allows you to use
predicate checkers like boolean variables. Once you call it, you'll be able to 
evaluate your predicates without passing the environ::

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
