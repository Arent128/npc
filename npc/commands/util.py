"""
Shared helpers and utility functions
"""

from os import path, walk
from contextlib import contextmanager
import sys

from npc.character import Character
from npc import settings

def create_path_from_character(character: Character, *, base_path=None, heirarchy=None, **kwargs):
    """
    Determine the best file path for a character.

    The path is created underneath base_path. It only includes directories
    which already exist. It's used by character creation, linting, and reorg.

    This function ignores tags not found in Character.KNOWN_TAGS.

    Args:
        character: Parsed character data
        base_path (str): Base path for character files
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Constructed file path based on the character data.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    if not base_path:
        base_path = prefs.get('paths.required.characters')
    if not heirarchy:
        heirarchy = prefs.get('paths.heirarchy')

    target_path = base_path

    # get raw heirarchy
    # split into pieces on '/'
    # iterate through pieces
    #
    # check for '?' operator
    #   split on '?'
    #   translate tag name if needed
    #   test tag presence
    #       most tags: has_tag(tag)
    #       foreign: foreign or wanderer
    #       type: not 'Unknown'
    #       *+ranks: any ranks exist
    #   if character has that tag, insert the literal
    #   end
    # translate tag name if needed
    # if the character has that tag:
    #   most tags: insert their value
    #   type: get 'types.type_key.type_path'
    #   groups: iterate group value in order, trying to add a new path component for each
    #   groups+ranks: iterate group values, add folder, iterate that group's ranks and add folders
    #   ranks: ignored and show a warning

    def _add_path_if_exists(base, potential):
        """Add a directory to the base path if that directory exists."""
        test_path = path.join(base, potential)
        if path.exists(test_path):
            return test_path
        return base

    for component in heirarchy.split('/'):
        if not(component.startswith('{') and component.endswith('}')):
            # No processing needed. Insert the literal and move on.
            target_path = _add_path_if_exists(target_path, component)
            continue

        component = component.strip('{}')
        if '?' in component:
            tag_name, literal = component.split('?')
            if tag_name == 'foreign':
                # "foreign?" gets special handling to check the wanderer tag as well
                if character.foreign:
                    target_path = _add_path_if_exists(target_path, literal)
            elif character.has_items(tag_name):
                target_path = _add_path_if_exists(target_path, literal)
            continue

    # # add type-based directory if we can
    # ctype = character.type_key
    # if ctype is not None:
    #     target_path = _add_path_if_exists(target_path, prefs.get('types.{}.type_path'.format(ctype), '.'))

    # # handle type-specific considerations
    # if ctype == 'changeling':
    #     # changelings use court first, then groups
    #     if 'court' in character:
    #         for court_name in character['court']:
    #             target_path = _add_path_if_exists(target_path, court_name)
    #     else:
    #         target_path = _add_path_if_exists(target_path, 'Courtless')

    # # foreigners get a special folder
    # if 'foreign' in character or 'wanderer' in character:
    #     target_path = _add_path_if_exists(target_path, 'Foreign')
    # if character.has_items('foreign'):
    #     target_path = _add_path_if_exists(target_path, character.get_first('foreign'))
    # if character.has_items('location'):
    #     target_path = _add_path_if_exists(target_path, character.get_first('location'))

    # # freeholds use their own folders
    # if 'freehold' in character:
    #     target_path = _add_path_if_exists(target_path, character.get_first('freehold'))

    # # everyone uses groups in their path
    # if 'group' in character:
    #     for group_name in character['group']:
    #         target_path = _add_path_if_exists(target_path, group_name)

    return target_path

def find_empty_dirs(root):
    """
    Find empty directories under root

    Args:
        root (str): Starting path to search

    Yields:
        Path of empty directories under `root`
    """
    for dirpath, dirs, files in walk(root):
        if not dirs and not files:
            yield dirpath

def sort_characters(characters, order=None):
    """
    Sort a list of Characters.

    Args:
        characters (list): Characters to sort.
        order (str|None): The order in which the characters should be sorted.
            Unrecognized sort orders are ignored. Supported orders are:
            * "last" - sort by last-most name (default)
            * "first" - sort by first name

    Returns:
        List of characters ordered as requested.
    """
    def last_name(character):
        """Get the character's last-most name"""
        return character.get_first('name', '').split(' ')[-1]

    def first_name(character):
        """Get the character's first name"""
        return character.get_first('name', '').split(' ')[0]

    if order is None:
        order = "last"

    if order == "last":
        return sorted(characters, key=last_name)
    elif order == "first":
        return sorted(characters, key=first_name)
    return characters

@contextmanager
def smart_open(filename=None, binary=False):
    """
    Open a named file or stdout as appropriate.

    This function is designed to be used in a `with` block.

    Args:
        filename (str|None): Name of the file path to open. None and '-' mean
            stdout.
        binary (bool): If opening a file, whether to open it in bytes mode. If
            opening stdout, whether to get its buffer.

    Yields:
        File-like object.

        When filename is None or the dash character ('-'), this function will
        yield sys.stdout. When filename is a path, it will yield the open file
        for writing.

    """
    if filename and filename != '-':
        stream = open(filename, 'wb') if binary else open(filename, 'w')
    else:
        stream = sys.stdout.buffer if binary else sys.stdout

    try:
        yield stream
    finally:
        if stream is not sys.stdout:
            stream.close()
