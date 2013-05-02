import logging
import os
import stat
import subprocess
import zc.buildout
from zc.recipe.egg.egg import Eggs

class Recipe(object):
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger(self.name)
        self.make_target_dir = False
        self.pip_exe = 'pip'

        if self.options.get('pip', None):
            self.pip_exe = self.options['pip']

    def install(self):
        reqs = self.options['requirements'].split()
        cwd = self.buildout["buildout"]["directory"]
        eggs_dir = self.buildout["buildout"]["eggs-directory"]
        location = os.path.join(
                self.buildout["buildout"]["parts-directory"],
                self.name
            )
        if not os.path.exists(location):
            os.mkdir(location)
        
        filename = os.path.join(location, 'requirements.txt')
        req_file = open(filename, 'w')
        req_file.write("\n".join(reqs))
        req_file.flush()
        arguments = [self.pip_exe, 'install', '--egg',]
        arguments += ['--install-option', '--install-purelib=%s' % eggs_dir]
        arguments += ['-r', 'parts/%s/requirements.txt' % self.name]
        env = {'PYTHONPATH': eggs_dir, 'PATH': os.environ['PATH']}

        if self.buildout['buildout']['offline'] != 'true':
            subprocess.check_call(arguments, env=env)

        disable_pth = self.options.get('disable-pth', 'false')
        if disable_pth in ('true', '1'):
            for filename in os.listdir(eggs_dir):
                if filename in ('site.py', 'site.pyc', 'easy-install.pth'):
                    os.remove(os.path.join(eggs_dir, filename))

        return self.options.created()

    def update(self):
        self.install()
