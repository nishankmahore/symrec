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
import symrec.callback as clb

from spacy.tokens.doc import Doc
from symrec.matcher import EntityMatcher
from symrec.callback import FINDING, DISORDER

__author__ = 'Aleksandar Savkov'

em = EntityMatcher()


class TestNonFindings:

    def test_normal(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fever'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, 0, 2, 3)]

        # use the last match to call the acceptor
        match_index = len(matches) - 1

        # call the acceptor func
        clb.ignore_non_findings(None, doc, match_index, matches)

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
        clb.ignore_non_findings(None, doc, match_index, matches)

        # extract the results
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = []

        assert test_matches == filtered_matches, 'Unexpected matches found.'


class TestAllMatches:

    def test_normal(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fracture'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, DISORDER, 2, 3)]

        # use the last match to call the acceptor
        match_index = len(matches) - 1

        # call the acceptor func
        clb.keep_matches(None, doc, match_index, matches)

        # extract the matches
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        assert test_matches == matches, 'Broken match filtering.'

    def test_not_last_call(self):

        # set up the document
        doc = Doc(em.matcher.vocab, words=['Backache', 'and', 'fracture'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, DISORDER, 2, 3)]

        # set the index to not the last match
        match_index = len(matches) - 2

        # call the acceptor func
        clb.keep_matches(None, doc, match_index, matches)

        # extract the results
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = []

        assert test_matches == filtered_matches, 'Unexpected matches found.'


class TestFirstDisorder:

    def test_normal(self):

        # set up the document
        doc = Doc(em.matcher.vocab,
                  words=['Backache', 'meningitis', 'fracture'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, DISORDER, 1, 2), (0, DISORDER, 2, 3)]

        # use the last match to call the acceptor
        match_index = len(matches) - 1

        # call the acceptor func
        clb.keep_first_disorder(None, doc, match_index, matches)

        # extract the matches
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = [(0, DISORDER, 1, 2)]

        assert test_matches == filtered_matches, 'Broken match filtering.'

    def test_not_last_call(self):
        # set up the document
        doc = Doc(em.matcher.vocab,
                  words=['Backache', 'meningitis', 'fracture'])

        # set up mock matches
        matches = [(0, FINDING, 0, 1), (0, DISORDER, 1, 2), (0, DISORDER, 2, 3)]

        # set the index to not the last match
        match_index = len(matches) - 2

        # call the acceptor func
        clb.keep_first_disorder(None, doc, match_index, matches)

        # extract the results
        test_matches = list([(0, e.label, e.start, e.end) for e in doc.ents])

        # set the expected result
        filtered_matches = []

        assert test_matches == filtered_matches, 'Unexpected matches found.'
