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

from spacy.tokens.doc import Doc
from symrec.matcher import EntityMatcher, parse_ctype, ignore_non_findings, \
    get_entity_params, FINDING

__author__ = 'Aleksandar Savkov'


em = EntityMatcher()
matches_jsn = json.loads('../res/matches.json')


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


class TestEntitiParams:

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


class TestAcceptor:

    def test_normal(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fever'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, 0, 2, 3)]

        # use the last match to call the acceptor
        match_index = len(matches) - 1

        # call the acceptor func
        ignore_non_findings(None, doc, match_index, matches)

        # extract the matches
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = [(0, FINDING, 0, 1)]

        assert test_matches == filtered_matches, 'Broken match filtering.'

    def test_not_last_call(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fever'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, 0, 2, 3)]

        # set the index to not the last match
        match_index = len(matches) - 2

        # call the acceptor func
        ignore_non_findings(None, doc, match_index, matches)

        # extract the results
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = []

        assert test_matches == filtered_matches, 'Unexpected matches found.'


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