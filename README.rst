Introduction
============

''mk.recipe.modwsgi'' is a `zc.buildout`_ recipe which creates
entry point for mod_wsgi_. It's based on ''collective.recipe.modwsgi''
but I decided to create it after failed to find recipe that generate
plain `mod_wsgi`_ script instead of one that use Paste.

It is very simple to use. This is a minimal ''buildout.cfg'' file
which creates a WSGI script mod_python can use::

    [buildout]
    parts = mywsgiapp

    [mywsgiapp]
    recipe = mk.recipe.modwsgi
    eggs = mywsgiapp
    wsgi-module = mywsgiapp.wsgi

This will create a small python script in parts/mywsgiapp called
''wsgi'' which mod_wsgi can load. You can also use the optional
''extra-paths'' option to specify extra paths that are added to
the python system path. The script will import `application` attribute
from the `wsgi-module` specified.

The apache configuration for this buildout looks like this::

    WSGIScriptAlias /mysite /home/me/buildout/parts/mywsgiapp/wsgi

    <Directory /home/me/buildout>
        Order deny,allow
        Allow from all
    </Directory>

If the python script must be accessed from somewhere else than the buildout
parts folder, you can use the optional ''target'' option to tell the recipe
where the script should be created.

For instance, the configuration for the mywsgiapp part could look like this::

    [mywsgiapp]
    recipe = collective.recipe.modwsgi
    eggs = mywsgiapp
    target = /var/www/myapp.wsgi
    wsgi-module = mywsgiapp.wsgi

The recipe would then create the script at /var/www/myapp.wsgi.

Note that the directory containing the target script must already exist on
the filesystem prior to running the recipe and be writeable.

The apache configuration for this buildout would then look like this::

    WSGIScriptAlias /mysite /var/www/myapp.wsgi

    <Directory /var/www>
        Order deny,allow
        Allow from all
    </Directory>

This recipe does not fully install packages, which means that console scripts
will not be created. If you need console scripts you can add a second
buildout part which uses `z3c.recipe.scripts`_ to do a full install.

.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout
.. _paste.deploy: http://pythonpaste.org/deploy/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _z3c.recipe.scripts: http://pypi.python.org/pypi/z3c.recipe.scripts
