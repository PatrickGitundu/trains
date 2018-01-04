"""
    KIwiland Trains App Tests
    ~~~~~~~~~~~~
    Tests the trains_flask application.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from setuptools import setup,find_packages

setup(
    name='trains',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask','networkx',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)