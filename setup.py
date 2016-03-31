#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

requirements = [
    'requests',
    'gitpython',
    'netaddr',
    'pyyaml',
    'boto',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='kubespray',
    version='0.2.5',
    description="Kubespray kubernetes cluster deployment",
    author="Smaine Kahlouch",
    author_email='smainklh@gmail.com',
    url='https://github.com/kubespray/kubespray',
    data_files=[
        ('/etc/kubespray', ['src/kubespray/files/kubespray.yml'])
    ],
    packages=find_packages('src'),
    scripts=[
        'bin/kubespray'
    ],
    package_dir={'': 'src'},
    package_data={'kubespray': ['files/*.yml'], },
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
