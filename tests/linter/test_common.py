import npc
import pytest
import os
from tests.util import fixture_dir

@pytest.fixture
def lint_output(capsys):
    def do_lint(charname, strict=False):
        search = fixture_dir('linter', 'characters', 'Humans', charname)
        npc.commands.lint(search, strict=strict)
        output, _ = capsys.readouterr()
        return output
    return do_lint

def test_requires_type(lint_output):
    assert "Missing type" in lint_output('Gotta Nada.nwod')

@pytest.mark.parametrize('charname', ['Gotta Nada.nwod', 'Gotta Type.nwod'])
def test_requires_description(lint_output, charname):
    assert "Missing description" in lint_output(charname)
