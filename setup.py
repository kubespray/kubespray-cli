#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'pyyaml',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='kubespray',
    version='0.1.0',
    description="Kubespray kubernetes cluster deployment",
    long_description=readme + '\n\n' + history,
    author="Smaine Kahlouch",
    author_email='smainklh@gmail.com',
    url='https://github.com/kubespray/kubespray',
    data_files=[
        ('/etc/kubespray', ['examples/kubespray.yml'])
    ],
    packages=[
        'kubespray',
    ],
    scripts=[
        'bin/kubespray'
    ],
    package_dir={'kubespray':
                 'kubespray'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='kubespray',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
