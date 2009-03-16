*******************************
**repoze.what-pylons** releases
*******************************

This document describes the releases of :mod:`repoze.what.plugins.pylonshq`.


.. _1.0rc4:

**repoze.what-pylons** 1.0rc4 (2009-03-16)
==========================================

* Added a couple of trivial functions:
  :func:`is_met <repoze.what.plugins.pylonshq.is_met>` and
  :func:`not_met <repoze.what.plugins.pylonshq.not_met>`.
* Added warnings on why "predicate booleanizers" should be avoided by all means.


.. _1.0rc3:

**repoze.what-pylons** 1.0rc3 (2009-03-04)
==========================================

* :class:`repoze.what.plugins.pylonshq.ControllerProtector` didn't support
  class instances. Fixed thanks to Alberto Valverde and Christopher Perkins!
* Functional test suite ported to **repoze.who-testutil** to ease maintenance.
* Documentation enhancements.


.. _1.0rc2:

**repoze.what-pylons** 1.0rc2 (2009-02-20)
==========================================

* This plugin requires ``decorator`` v3.0 or better, but no minimum version
  was required. Reported by Binet Bruno.


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
