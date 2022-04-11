from git_remote_ipfs.util import (
    Config,
    stderr,
)
from git_remote_ipfs.helper import Helper

import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def error(msg):
    stderr("error: %s\n" % msg)
    exit(1)


def get_helper(url):
    """
    Return a Helper configured to point at the given URL.

    URLs are one of:
        dropbox:///path/to/repo
        dropbox://username@/path/to/repo
        dropbox://:token@/path/to/repo
    """
    return Helper(url)
