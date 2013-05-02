Introduction
============

''mk.recipe.pip'' is a `zc.buildout`_ recipe which allow
you to piggyback on pip to install certain packages that
not possible to install using `zc.recipe.egg`_. It does not
replace `zc.recipe.egg`_ (not yet) but should be used in conjuction
with that recipe. It's based on ''collective.recipe.modwsgi'.'

It is very simple to use. This is a minimal ''buildout.cfg'' file::

    [buildout]
    parts = pip base

    [pip]
    recipe = mk.recipe.pip
    requirements =
        svn+http://django-grappelli.googlecode.com/svn/trunk
    disable-pth = true

    [base]
    recipe = zc.recipe.egg
    interpreter = python
    eggs =
        grappelli
        Django==1.5.1

Above, ``grappelli`` will be installed into ``eggs`` directory so that
`zc.recipe.egg`_ can pick it up. This especially usefull to install private
packages that only available maybe through svn or other version control system.

.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout
.. _zc.recipe.egg: http://pypi.python.org/pypi/zc.recipe.egg
.. _paste.deploy: http://pythonpaste.org/deploy/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _z3c.recipe.scripts: http://pypi.python.org/pypi/z3c.recipe.scripts
