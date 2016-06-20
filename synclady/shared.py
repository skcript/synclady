# -*- encoding: utf-8 -*-

import re

# Find if path is hidden
def is_hidden(path):
    """Regex matches a path to find if it is hidden"""
    m = re.search('(?<=\/\.)\w+', path)
    return m is not None
