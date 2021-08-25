import subprocess

import requests

from .constants import *
from .. import __version__


def try_upgrade():
    try:
        r = requests.get('https://pypi.org/pypi/codeforces-toolbox/json')
        r.raise_for_status()
    except requests.RequestException:
        return
    latest_version = r.json()['info']['version']
    if __version__ != latest_version:
        print(warning_style(f'The new version ({latest_version}) is available. You should install it using '
                            f'`pip install --upgrade codeforces-toolbox`'))
        d = input('Do you want to try auto-upgrade? [y/n] ')
        if d.lower() in ('y', 'yes'):
            s = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'codeforces-toolbox'],
                               stdout=subprocess.DEVNULL)
            if s.returncode != 0:
                print(error_style('Installation failed.\n'))
            else:
                print(info_style('Installation was successful.\n'))
        else:
            print('')
