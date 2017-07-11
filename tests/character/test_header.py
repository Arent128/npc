"""Tests the intricacies of the build_header method"""

import re

import npc
import pytest

class TestName:
    def test_not_in_path(self):
        char = npc.Character(name=['Hugh Mann'], path='local/storage/fake.nwod')
        header = char.build_header()
        assert "@realname Hugh Mann" in header

    def test_in_path(self):
        char = npc.Character(name=['Hugh Mann'], path='local/storage/Hugh Mann.nwod')
        header = char.build_header()
        assert "@realname Hugh Mann" not in header

    def test_many_names(self):
        names = ['Hugh Mann', 'Mr. Big', 'Huggy Bug']
        char = npc.Character(name=names)
        header = char.build_header()
        assert "@name {}".format(names[0]) not in header
        for name in names[1:]:
            assert "@name {}".format(name) in header

class TestShortcuts:
    def test_seeming_and_kith(self):
        char = npc.Character(type=['Changeling'], seeming=['Beast'], kith=['Swimmerskin'])
        header = char.build_header()
        assert "@changeling Beast Swimmerskin" in header

    def test_no_seeming(self):
        char = npc.Character(type=['Changeling'], kith=['Swimmerskin'])
        header = char.build_header()
        assert "@type Changeling" in header
        assert "@kith Swimmerskin" in header

    def test_no_kith(self):
        char = npc.Character(type=['Changeling'], seeming=['Beast'])
        header = char.build_header()
        assert "@type Changeling" in header
        assert "@seeming Beast" in header

@pytest.mark.parametrize('flag', npc.Character.BARE_FLAGS)
def test_bare_flag(flag):
    char = npc.Character()
    char.append(flag, None)
    header = char.build_header()
    assert re.search(r'@{}$'.format(flag), header, re.MULTILINE)

@pytest.mark.parametrize('flag', npc.Character.DATA_FLAGS)
def test_data_flag(flag):
    char = npc.Character()
    char.append(flag, None)
    assert re.search(r'@{}$'.format(flag), char.build_header(), re.MULTILINE)
    char.append(flag, 'datas')
    assert re.search(r'@{} datas$'.format(flag), char.build_header(), re.MULTILINE)

singletons = ('name', 'type', 'seeming', 'kith')
@pytest.mark.parametrize('tag', [tag for tag in npc.Character.TAGS if tag not in singletons])
def test_tag_for_all(tag):
    char = npc.Character()
    bits = ['some', 'words', 'and', 'stuff']
    for bit in bits:
        char.append(tag, bit)
    header = char.build_header()
    for bit in bits:
        assert '@{} {}'.format(tag, bit) in header

def test_rank():
    char = npc.Character()
    char.append('group', 'Townies')
    ranks = ['Foozer', 'Roz', 'Bazanger']
    for rank in ranks:
        char.append_rank('Townies', rank)
    header = char.build_header()
    for rank in ranks:
        assert '@rank {}'.format(rank) in header

def test_description():
    desc = 'Fee fie fo fum! I smell the blood of an Englishman!'
    char = npc.Character(description=desc)
    assert desc in char.build_header()