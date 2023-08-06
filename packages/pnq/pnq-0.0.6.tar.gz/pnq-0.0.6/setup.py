# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pnq',
    'version': '0.0.6',
    'description': '',
    'long_description': '# pnq\nPNQ is a Python implementation like Language Integrated Query (LINQ).\n\n# Requirement\n\n- Python 3.7+\n\n# Installation\n\n``` shell\npip install pnq\n```\n\n# Getting started\n\n\n# Setup\n\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
