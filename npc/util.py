#!/usr/bin/env python3.5

import re
import json
import sys

def load_json(filename):
    """ Parse a JSON file
        First remove all comments, then use the standard json package

        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )
    with open(filename) as f:
        content = ''.join(f.readlines())

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        # Return parsed json
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as e:
            e.nicemsg = "Bad syntax in '{0}' line {2} column {3}: {1}".format(filename, e.msg, e.lineno, e.colno)
            raise e
        except Exception as e:
            e.nicemsg = "Could not load '{0}': {1}".format(filename, e.msg)
            raise e

def error(*args, **kwargs):
    print(*args, file=sysstderr, **kwargs)
