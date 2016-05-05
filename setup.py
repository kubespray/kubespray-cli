#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

requirements = [
    'requests',
    'netaddr',
    'markupsafe',
    'pyyaml',
    'boto',
    'apache-libcloud'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='kargo',
    version='0.3.2',
    description="Kargo kubernetes cluster deployment",
    author="Smaine Kahlouch",
    author_email='smainklh@gmail.com',
    url='https://github.com/kargo/kargo',
    data_files=[
        ('/etc/kargo', ['src/kargo/files/kargo.yml'])
    ],
    packages=find_packages('src'),
    scripts=[
        'bin/kargo'
    ],
    package_dir={'': 'src'},
    package_data={'kargo': ['files/*.yml'], },
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='kargo',
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
