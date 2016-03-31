#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Kargo.
#
#    Foobar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import logging
import shutil
import os
import sys
from git import Repo
from ansible.utils.display import Display
from subprocess import PIPE, STDOUT, Popen, CalledProcessError
display = Display()


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def query_yes_no(question, default="yes"):
    """Question user input 'Yes' or 'No'"""
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please answer with 'yes' or 'no' (or 'y' or 'n').\n"
            )


def get_logger(logfile, loglevel):
    logger = logging.getLogger()
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, loglevel.upper()))
    return logger


def clone_git_repo(name, directory, git_repo):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    display.banner('CLONING %s GIT REPO' % name.upper())
    Repo.clone_from(git_repo, directory)
    display.display('%s repo cloned' % name, color='green')


def run_command(description, cmd):
    '''
    Execute a system command
    '''
    try:
        proc = Popen(
            cmd, stdout=PIPE, stderr=STDOUT,
            universal_newlines=True, shell=False
        )
        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                print(line),
        proc.wait()
        return(proc.returncode, None)
    except CalledProcessError as e:
        display.error('%s: %s' % (description, e.output))
        emsg = e.message
        return(proc.returncode, emsg)
