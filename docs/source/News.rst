*******************************
**repoze.what-pylons** releases
*******************************

This document describes the releases of :mod:`repoze.what.plugins.pylonshq`.


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
