*******************************
**repoze.what-pylons** releases
*******************************

This document describes the releases of :mod:`repoze.what.plugins.pylonshq`.


.. _1.0rc1:

**repoze.what-pylons** 1.0rc1 (2009-02-19)
==========================================

* Now :mod:`repoze.what` predicates can be evaluated without passing the
  ``environ`` explicitly, thanks to 
  :func:`repoze.what.plugins.pylonshq.booleanize_predicates`. This *magical*
  functionality can be disabled with
  :func:`repoze.what.plugins.pylonshq.debooleanize_predicates`.


.. _1.0b3:

**repoze.what-pylons** 1.0b3 (2009-02-16)
=========================================

* Now :class:`repoze.what.plugins.pylonshq.ActionProtector` is a signature
  preserving decorator. This means that now Pylons users can have positional 
  and named arguments in their controller actions.


.. _1.0b2:

**repoze.what-pylons** 1.0b2 (2009-02-11)
=========================================

* The :class:`repoze.what.plugins.pylonshq.ActionProtector` decorator made
  the decorated function ignore its decorators defined after 
  ``@ActionProtector``. Thanks to Florent Aide and Alberto Valverde for finding
  the bug and proposing the solution, respectively.


.. _1.0b1:

**repoze.what-pylons** 1.0b1 (2009-02-09)
=========================================

This is the first release of **repoze.what-pylons** as an
independent project. Much of the initial functionality has been taken from
the `TurboGears v2.0 project <http://turbogears.org/2.0/>`_.

* Created a decorator similar to the former TurboGears' ``@require``, but
  improved: :class:`repoze.what.plugins.pylonshq.ActionProtector`. As of
  TurboGears v2.0b6, its ``@require`` decorator is a subclass of this
  decorator.
* Introduced the class decorator for controller-wide authorization
  :class:`repoze.what.plugins.pylonshq.ControllerProtector`.
