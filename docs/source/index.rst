********************************************************
The :mod:`repoze.what` plugin for Pylons/TG2 integration
********************************************************

:Author: Gustavo Narea.
:Latest release: |release|

.. module:: repoze.what.plugins.pylons
    :synopsis: Ready-to-use authentication and authorization
.. moduleauthor:: Gustavo Narea <me@gustavonarea.net>

.. topic:: Overview

    This plugin allows you to take advantage of a rather simple, and usual, 
    authentication and authorization setup, in which the users' data, the 
    groups and the permissions used in the application are all stored in a 
    SQLAlchemy or Elixir-managed database.
    
    Put simply, it configures :mod:`repoze.who` and :mod:`repoze.what` in one
    go so that you can have an authentication and authorization system working
    quickly -- hence the name.


How to install
==============

The minimum requirements are SQLAlchemy, :mod:`repoze.who.plugins.sa`,
:mod:`repoze.what` and :mod:`repoze.what.plugins.sql`, and you can install it 
all with ``easy_install``::
    
    easy_install repoze.what-quickstart

The development mainline is available at the following Subversion repository::

    http://svn.repoze.org/repoze.what/plugins/quickstart/trunk/


How to use it
=============

To get started quickly, you may copy the SQLAlchemy-powered model 
defined in `model_sa_example.py 
<http://code.gustavonarea.net/repoze.what-quickstart/_static/model_sa_example.py>`_
(or `model_elixir_example.py 
<http://code.gustavonarea.net/repoze.what-quickstart/_static/model_elixir_example.py>`_
for Elixir) and then create at least a few rows to try it out::

    u = User()
    u.user_name = u'manager'
    u.password = u'managepass'

    DBSession.save(u)

    g = Group()
    g.group_name = u'managers'

    g.users.append(u)

    DBSession.save(g)

    p = Permission()
    p.permission_name = u'manage'
    p.groups.append(g)

    DBSession.save(p)
    DBSession.flush()

Now that you have some rows in your database, you can set up authentication
and authorization as explained in the next section.


How to set it up
----------------

Although this is a :mod:`repoze.what` plugin and :mod:`repoze.what` is meant 
to deal with authorization only, this module configures authentication and
identification for you through :mod:`repoze.who` as well.

Such a setup is performed by the :func:`setup_sql_auth` function:

.. autofunction:: setup_sql_auth

See "`changing attribute names`_" to learn how to use the ``translations``
argument in :func:`setup_sql_auth`.


Customizing the model definition
--------------------------------

Your auth-related model doesn't `have to` be like the default one, where the
class for your users, groups and permissions are, respectively, ``User``,
``Group`` and ``Permission``, and your users' user name is available in
``User.user_name``. What if you prefer ``Member`` and ``Team`` instead of
``User`` and ``Group``, respectively? Or what if you prefer ``Group.members``
instead of ``Group.users``? Read on!

Changing class names
~~~~~~~~~~~~~~~~~~~~

Changing the name of an auth-related class (``User``, ``Group`` or ``Permission``)
is a rather simple task. Just rename it in your model, and then make sure to
update the parameters you pass to :func:`setup_sql_auth` accordingly.

Changing attribute names
~~~~~~~~~~~~~~~~~~~~~~~~

You can also change the name of the attributes assumed by
:mod:`repoze.what` in your auth-related classes, such as renaming
``User.groups`` to ``User.memberships``.

Changing such values is what :mod:`repoze.what` calls "translating".
You may set the translations for the attributes of the models
:mod:`repoze.what` deals with in a dictionary passed to :func:`setup_sql_auth`
as its ``translations`` parameters. For
example, if you want to replace ``Group.users`` with ``Group.members``, you may
use the following translation dictionary::

    translations['users'] = 'members'

Below are the translations that you would be able to set in the ``translations``
dictionary used above:

    * ``user_name``: The translation for the attribute in ``User.user_name``.
    * ``users``: The translation for the attribute in ``Group.users``.
    * ``group_name``: The translation for the attribute in ``Group.group_name``.
    * ``groups``: The translation for the attribute in ``User.groups`` and
      ``Permission.groups``.
    * ``permission_name``: The translation for the attribute in
      ``Permission.permission_name``.
    * ``permissions``: The translation for the attribute in ``User.permissions``
      and ``Group.permissions``.
    * ``validate_password``: The translation for the method in
      ``User.validate_password``.


:mod:`repoze.who` plugins
-------------------------

This plugin defines the following :mod:`repoze.who` plugins:

.. autoclass:: FriendlyRedirectingFormPlugin
    :members: __init__


How to get help?
================

The prefered place to ask questions is the `Repoze mailing list 
<http://lists.repoze.org/listinfo/repoze-dev>`_ or the `#repoze 
<irc://irc.freenode.net/#repoze>`_ IRC channel. Bugs reports and feature 
requests should be sent to `the issue tracker of the Repoze project 
<http://bugs.repoze.org/>`_.

Contents
========

.. toctree::
    :maxdepth: 2

    News


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
