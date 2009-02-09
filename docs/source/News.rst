******************************************
:mod:`repoze.what.plugins.pylons` releases
******************************************

This document describes the releases of :mod:`repoze.what.plugins.pylons`.


.. _1.0b1:

:mod:`repoze.what.plugins.pylons` 1.0b1 (*unreleased*)
======================================================

This is the first release of :mod:`repoze.what.plugins.pylons` as an
independent project. Much of the initial functionality has been taken from
the `TurboGears v2.0 project <http://turbogears.org/2.0/>`_.

* Adapted the TurboGears' ``@require`` decorator and turned into
  :class:`repoze.what.plugins.pylonshq.decorators.ActionProtectionDecorator`.
* Introduced the class decorator for controller-wide authorization
  :class:`repoze.what.plugins.pylonshq.decorators.ControllerProtectionDecorator`.
