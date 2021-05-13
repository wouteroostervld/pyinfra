from pyinfra.api import FactBase

from .util.packaging import parse_packages
import re


class PkgPackages(FactBase):
    '''
    Returns a dict of installed pkg packages:

    .. code:: python

        {
            'package_name': ['version'],
        }
    '''

    command = 'pkg info || pkg_info || true'
    regex = r'^([a-zA-Z0-9_\-\+]+)\-([0-9a-z\.]+)'
    default = dict

    def process(self, output):
        return parse_packages(self.regex, output)

class PkgFreshPackages(FactBase):
    '''
    Returns the list of fresh pkg packages:
    .. code:: python
        
        {
            'fresh_packages': ['sudo-1.9.5'],
        }
    '''
    command = '[ `uname -s` == \'FreeBSD\' ] && pkg upgrade -qn || true'
    regex = r'([a-zA-Z0-9_\-\+]+): ([0-9a-z\._]+) -> ([0-9a-z\.+_])'

    def process(self, output):
        result = {}
        for line in output: 
            match = re.search(self.regex, line)
            if match:
                pkg_name, pkg_version_old, pkg_version_new = match.groups()
                result[pkg_name]={
                    'old_version': pkg_version_old,
                    'new_version': pkg_version_new,
                }
        return result
