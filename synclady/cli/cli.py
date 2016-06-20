# -*- encoding: utf-8 -*-
"""
Synclady command line tool
"""

import click

from synclady import Synclady

# Disable the warning that Click displays (as of Click version 5.0) when users
# use unicode_literals in Python 2.
# See http://click.pocoo.org/dev/python3/#unicode-literals for more details.
click.disable_unicode_literals_warning = True

@click.group()
def main():
    """Synclady command line tool."""
    pass

@main.command()
def sync():
    """Starts file listener"""
    Synclady.sync()

@main.command()
def resync():
    """Brings local and server to sync"""
    Synclady.resync()

@main.command()
def pull():
    """Brings local and server to sync"""
    Synclady.pull()
