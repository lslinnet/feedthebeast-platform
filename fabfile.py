# This fabfile is a useful way of handling
# builds and deployments. It is not at all required,
# but quite handy. Find out more about fabric on
# http://fabfile.org/

from __future__ import with_statement
from fabric.api import local, settings, abort, run
from fabric.contrib.console import confirm
from os import path, mkdir
from time import time

# Rebuilding takes time so we probably want to
# avoid doing it unnecessarily. In order to avoid unnecessary rebuilds,
# we can store md5sums for files that specify the projects we should fetch.
# Add all of those files here.
check_files = ["platform.make"]

def build():
    """
    Build this project.
    """
    # Save any old build
    if path.isdir('web'):
        local('mv web web-old')
        local('chmod -R +w web-old/sites')
    local('drush make --working-copy platform.make web')
    # Move all sites from the old web directory to the new one.
    if path.isdir('web-old'):
        local('rm -rf web-old/sites/all')
        local('mv web/sites/all web-old/sites/.')
        local('rm -rf web/sites')
        local('mv web-old/sites web/sites')
        local('rm -rf web-old')
    save_sums()
    # If you have more things that you want to do, you can just add more
    # commands here.

def clean():
    """
    Clean this project up.
    """
    local("rm -rf web")

def rebuild():
    """
    Rebuild this project.
    """
    if not path.isdir('web'):
        print "This project does not have build yet. Building..."
        build()
    elif not check_build():
        build()
    else:
        print "Rebuild not necessary."

def check_build():
    print "Verifying checksums..."
    for check_file in check_files:
        if not check_sum(check_file):
            print "Checksums does not match for {0}".format(check_file)
            return False
    print "All good."
    return True

def check_sum(check_file):
    new_sum = get_checksum(check_file)
    old_sum_file = '.checksums/{0}'.format(check_file)
    # We obviously need to rebuild if the file is missing.
    if not path.isfile(old_sum_file):
        return False
    with open(old_sum_file, 'r') as f:
        old_sum = f.readline()
        if new_sum != old_sum:
            return False
    return True

def get_checksum(check_file):
    """
    Get the checksum of a file.
    """
    import hashlib
    md5 = hashlib.md5()
    with open(check_file, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), ''):
            md5.update(chunk)
    return md5.digest()

def save_sums():
    if not path.isdir('.checksums'):
        mkdir('.checksums')
    for check_file in check_files:
        new_sum = get_checksum(check_file)
        old_sum_file = '.checksums/{0}'.format(check_file)
        with open(old_sum_file, 'w') as f:
            f.write(new_sum)
