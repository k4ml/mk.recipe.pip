import logging
import os
import stat
import zc.buildout
from zc.recipe.egg.egg import Eggs

WRAPPER_TEMPLATE = """\
import sys
syspaths = [
    %(syspath)s,
    ]

for path in reversed(syspaths):
    if path not in sys.path:
        sys.path[0:0]=[path]

%(initialization)s

from %(wsgi_module)s import application

%(finalization)s
"""


class Recipe(object):
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger(self.name)
        self.make_target_dir = False

        if "wsgi-module" not in options:
            self.logger.error(
                    "You need to specify import path to module containing "
                    "your wsgi application")
            raise zc.buildout.UserError("No wsgi module given")

        if self.options.get("makedir", "false") == "true":
            self.make_target_dir = True

        if "target" in options:
            self.location = os.path.dirname(options["target"])
            if not os.path.isdir(self.location) and not self.make_target_dir:
                self.logger.error(
                    "The 'target' option refers to a directory that is not "
                    "valid: %s and makedir option not set or false" % self.location)
                raise zc.buildout.UserError("Invalid directory for target")

    def install(self):
        egg = Eggs(self.buildout, self.options["recipe"], self.options)
        reqs, ws = egg.working_set()
        path = [pkg.location for pkg in ws]
        extra_paths = self.options.get('extra-paths', '')
        extra_paths = extra_paths.split()
        path.extend(extra_paths)

        output = WRAPPER_TEMPLATE % dict(
            wsgi_module=self.options["wsgi-module"],
            syspath=",\n    ".join((repr(p) for p in path)),
            initialization=self.options.get('initialization', ''),
            finalization=self.options.get('finalization', ''),
            )

        target = self.options.get("target")
        if target is None:
            location = os.path.join(
                            self.buildout["buildout"]["parts-directory"],
                            self.name)
            if not os.path.exists(location):
                os.mkdir(location)
                self.options.created(location)
            target = os.path.join(location, "wsgi")
        else:
            outputdir, filename = os.path.split(os.path.realpath(target))
            if not os.path.exists(outputdir) and self.make_target_dir:
                os.makedirs(outputdir)
            self.options.created(target)

        f = open(target, "wt")
        f.write(output)
        f.close()

        exec_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(target, os.stat(target).st_mode | exec_mask)
        self.options.created(target)

        return self.options.created()

    def update(self):
        self.install()
