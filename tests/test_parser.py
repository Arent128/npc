import npc
import pytest
import itertools
from tests.util import fixture_dir

from npc.character.tags import UnknownTag

def test_remove_filename_comments():
    parseables = fixture_dir('parsing', 'characters', 'Fetches', 'macho mannersson - faker.nwod')
    characters = list(npc.parser.get_characters(search_paths=[parseables]))
    assert characters[0].tags('name')[0] == 'macho mannersson'

class TestSpecialCharacters:

    def test_allow_apostrophes_in_names(self):
        parseables = fixture_dir('parsing', 'characters', 'Fetches', "manny o'mann - super faker.nwod")
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        assert characters[0].tags('name')[0] == "manny o'mann"

    def test_allow_periods_in_names(self):
        parseables = fixture_dir('parsing', 'characters', 'Fetches', "Dr. Manny Mann - fakier.nwod")
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        assert characters[0].tags('name')[0] == "Dr. Manny Mann"

    def test_allow_hyphens_in_names(self):
        parseables = fixture_dir('parsing', 'characters', 'Fetches', "Manny Manly-Mann - fakiest.nwod")
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        assert characters[0].tags('name')[0] == "Manny Manly-Mann"

    def test_allow_commas_in_names(self):
        parseables = fixture_dir('parsing', 'characters', 'Fetches', "Manners Mann, Ph.D. - fakierest.nwod")
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        assert characters[0].tags('name')[0] == "Manners Mann, Ph.D."

class TestInclusion:
    """Tests which files are included in the parsed data"""

    def test_ignore_dir(self):
        parseables = fixture_dir('parsing', 'characters')
        ignore_me = fixture_dir('parsing', 'characters', 'Fetches')
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        for c in characters:
            assert c.tags('type')[0] != 'Fetch'

    def test_ignore_file(self):
        parseables = fixture_dir('parsing', 'characters')
        ignore_me = fixture_dir('parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod')
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        for c in characters:
            assert 'Kabana Matansa' not in c.tags['name']

    def test_conflict_dir(self):
        """Ignore a directory when it is in both the search and ignore lists"""
        parseables = fixture_dir('parsing', 'characters')
        ignore_me = fixture_dir('parsing', 'characters')
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        assert not len(list(characters))

    def test_conflict_file(self, ):
        """Always parse a file when it is in the search and ignore lists"""
        parseables = fixture_dir('parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod')
        ignore_me = fixture_dir('parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod')
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        assert len(list(characters)) == 1

class TestTags:
    """Tests the behavior of specific tags.

    Basic tag inclusion is handled above.
    """

    @pytest.fixture
    def character(self):
        def make_character(filename):
            parseables = fixture_dir('parsing', 'tags', filename)
            characters = list(npc.parser.get_characters(search_paths=[parseables]))
            return characters[0]
        return make_character

    @pytest.fixture
    def basic_character(self, character):
        return character('Basic.nwod')
    
    @pytest.fixture
    def mutant_tests_character(self, character):
        return character('Jerry.nwod')

    def test_simple_tag(self, basic_character):
        """Tags should be added by name"""
        assert 'appearance' in basic_character.tags

    def test_unknown_tag(self, basic_character):
        """Unknown tags should be added"""
        assert 'unrecognized' in basic_character.tags

    def test_bare_tag(self, basic_character):
        """Tags with no data should be added"""
        assert 'skip' in basic_character.tags

    #MUTANT TEST
    #Tests the mutant that alters the tag decription 
    #
    def test_description_tag(self, basic_character):
        assert 'description' in basic_character.tags
#    # Test to see if it kills a mutant that altered the way empty lines
#    # were inserted into the discription
#    def test_line_empty(self, mutant_tests_character):
#        """@realname should overwrite the first name entry"""
#        assert mutant_tests_character.tags('description') == []
    #END OF MUTANT TEST
    
    def test_comment(self, basic_character):
        assert '#comment' not in basic_character.tags

    def test_foreign(self, basic_character):
        assert 'foreign' in basic_character.tags

    def test_changeling_shortcut(self, character):
        """@changeling should set type, seeming, and kith"""
        c = character('Changeling Tag.nwod')
        assert c.tags('type')[0] == 'Changeling'
        assert c.tags('seeming')[0] == 'Beast'
        assert c.tags('kith')[0] == 'Hunterheart'

    def test_realname(self, character):
        """@realname should overwrite the first name entry"""
        c = character('File Name.nwod')
        assert c.tags('name')[0] == 'Real Name'

    def test_group_rank(self, character):
        """@rank should scope its value to the most recent @group"""
        c = character('Group Rank.nwod')
        assert 'Brother' in c.tags('group')['Frat']

    def test_bare_rank(self, character):
        """when there's a bare rank with no group, it gets added to the top level as an UnknownTag"""
        c = character('Bare Rank.nwod')
        assert type(c.tags['rank']) == UnknownTag

class TestNames:
    """Tests the way character names are grabbed from filenames"""

    @pytest.fixture
    def character(self):
        def make_character(filename):
            parseables = fixture_dir('parsing', 'names', filename)
            characters = list(npc.parser.get_characters(search_paths=[parseables]))
            return characters[0]
        return make_character

    def test_notes(self, character):
        c = character('Standard Dude - dude man.nwod')
        assert c.tags('name')[0] == 'Standard Dude'

    def test_doctor(self, character):
        c = character('Dr. Manly Mann.nwod')
        assert c.tags('name')[0] == "Dr. Manly Mann"

class TestHiding:
    @pytest.fixture
    def character(self):
        def make_character(filename):
            parseables = fixture_dir('parsing', 'tags', filename)
            characters = list(npc.parser.get_characters(search_paths=[parseables]))
            return characters[0]
        return make_character

    def test_hide_marks_right_tag_as_hidden(self, character):
        c = character('Hidden Dead.nwod')
        assert c.tags('dead').hidden

    def test_hide_single_tag_value(self, character):
        c = character('Hidden Tags.nwod')
        assert c.tags('title').hidden_values == ['Yer Majesty']

    def test_hide_single_group(self, character):
        c = character('Hidden Tags.nwod')
        assert c.tags('group').hidden_values == ['Frat']

    def test_hide_group_subtags(self, character):
        c = character('Hidden Tags.nwod')
        assert c.tags('group').subtag('Divers').hidden == True

    def test_hide_single_subtag(self, character):
        c = character('Hidden Tags.nwod')
        assert c.tags('group').subtag('Seamen').hidden_values == ['Rower']
    
class TestMutations:
    # This test kills the mutations dealing  with the pasrsers support
    # of valid extentions
    # This should be killing mutants 1 - 4 on mutmut, which changes
    # the valid extention types
    def test_ignore_type(self):
        parseables = fixture_dir('parsing', 'characters', 'Changelings')
        testPath = fixture_dir('parsing', 'characters', 'Changelings')
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[testPath])
        assert len(list(characters)) == 7

    # This test kills the mutation dealing with the parsing of files
    # that do not have a extention to the filename
    # kills 27 in mutmut
    def test_invaild_extension_with_bare_true(self):
        #search_paths = []
        parseables = fixture_dir('parsing', 'characters', 'Changelings')
        testPath = fixture_dir('parsing', 'characters', 'Goblins')
        search_paths=[parseables]
        characters = list(itertools.chain.from_iterable((npc.parser._parse_path(path, ignore_paths=[], include_bare=True) for path in search_paths)))
        assert len(list(characters)) == 8

    # This test was to verify if the muypy tool was faulty compared to 
    # the mutmut tool
    def test_invaild_extension_with_bare_false(self):
        #search_paths = []
        parseables = fixture_dir('parsing', 'characters', 'Changelings')
        testPath = fixture_dir('parsing', 'characters', 'Goblins')
        search_paths=[parseables]
        characters = list(itertools.chain.from_iterable((npc.parser._parse_path(path, ignore_paths=[]) for path in search_paths)))
        for c in characters:
           assert 'Urgesh' not in c.tags['name']

