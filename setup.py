# -*- coding: utf-8 -*-
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'humax', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    author='Radomír Bosák',
    author_email='radomir.bosak@gmail.com',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Humax router CLI',
    download_url='https://github.com/radomirbosak/humax/archive/' \
                 + about['__version__'] + '.tar.gz',
    entry_points={
        'console_scripts': [
            'humax = humax.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        "requests",
        "pygments",
        "pyxdg",
    ],
    keywords=['humax', 'cli'],
    license='MIT',
    name='humax',
    packages=['humax'],
    url='https://github.com/radomirbosak/humax',
    version=about['__version__'],
)
