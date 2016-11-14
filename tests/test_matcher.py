# This file is part of SymptomRecogniser.
#
# SymptomRecogniser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SymptomRecogniser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SymptomRecogniser.  If not, see <http://www.gnu.org/licenses/>.
import json

from spacy.attrs import LOWER
from spacy.matcher import Matcher
from spacy.tokens.doc import Doc
from symrec.callback import FINDING, keep_matches
from symrec.matcher import EntityMatcher, parse_ctype, get_entity_params

__author__ = 'Aleksandar Savkov'


em = EntityMatcher()
matches_fh = open('../res/matches.json', 'r')
matches_jsn = json.load(matches_fh)


class TestCtypes:

    def test_normal(self):
        assert parse_ctype('Term text (term type)') == 'term type', \
            'Basic case of head term type not recognised.'

    def test_none(self):
        assert parse_ctype('Term text') is None, 'False positive recognition.'

    def test_parentheses(self):
        assert parse_ctype('Term text (optional), more text (term type)'),\
            'Likely confusion with other text in parentheses.'

    def test_extra_space(self):
        assert parse_ctype('Term text (term type) '), 'Problem with extra space'


class TestEntityParams:

    def test_normal(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fever'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, FINDING, 2, 3)]

        # assign the matches to the ents iterator
        doc.ents = matches

        # call the func
        test_jsn = list(get_entity_params(doc))

        # set the expected value
        jsn = matches_jsn['entities']

        assert jsn == test_jsn, 'Missing or unexpected matches found.'

    def test_none(self):
        # set up the document
        doc = Doc(em.matcher.vocab, words=['I', 'am', 'still', 'here'])

        # call the func
        test_jsn = list(get_entity_params(doc))

        assert [] == test_jsn, 'Unexpected matches found.'


def test_simple_matching():

    # load a simple pattern to the matcher
    # method resambles `load_snomedct`
    patterns = [
        [{LOWER: 'back'}, {LOWER: 'pain'}]
    ]
    key = 'test-id'
    ctype = 'TEST'
    atts = {'code': 'test-code', 'term': 'back pain'}

    em.matcher.add_entity(key, atts, on_match=keep_matches)
    for token_specs in patterns:
        em.matcher.add_pattern(key, token_specs, label=ctype)

    # prepare a sample sentece
    text = 'A sentence with back pain other pain and some back thoughts.'

    # extract the matches
    test_matches = em.match(text)

    # the only match should be this
    matches = [
        {
            'end_char': 25,
            'end_token': 5,
            'label': 'TEST',
            'start_char': 16,
            'start_token': 3,
            'text': 'back pain'
        }
    ]

    assert test_matches == matches, 'Unexpected matches in basic matching test.'

    # wipe the matcher clean
    em.matcher = Matcher(em.nlp.vocab)


# it is important that this test remains at the end, unless otherwise necessary
def test_snomed_matching():

    text = """
    The common symptoms of the disease are: high fever, night sweating,
    joint pain, and fatigue. Some other less common ones are dizziness and
    nausea.
    """

    # load the terms
    em.load_snomedct()

    # match the terms
    test_matches = em.match(text)

    # set the expected values
    matches = matches_jsn['snomedct']

    assert test_matches == matches, 'Unexpected matches in SNOMEDCT test.'
