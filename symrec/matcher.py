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
import argparse
import re

import spacy
from pymedtermino.snomedct import SNOMEDCT
from spacy.attrs import LOWER
from spacy.matcher import Matcher
from symrec.scraper import scrape

__author__ = 'Aleksandar Savkov'


FINDING = 104190


def parse_ctype(head_term):
    """Retrieves the type of the term based on the head term representation
    of SNOMEDCT terms in ``pymedtermino``.

    :param head_term: SNOMEDCT main term representation in ``pymedtermino``
    :type head_term: str
    :return: term type
    :rtype: str
    """

    m = re.match('^.+\((?P<type>[^)]+)\)$', head_term.strip())
    try:
        return m.group('type').strip()
    except AttributeError:
        return None


def ignore_non_findings(matcher, doc, i, matches):
    """A callback function that is called for all matches. Currently, it filters
    out all but the `FINDING` matches, and assigns the matches to the entities
    iterator.

    :param matcher: spaCy matcher
    :type matcher: spacy.matcher.Matcher
    :param doc: spaCy document
    :type doc: spacy.tokens.doc.Doc
    :param i: current match index
    :type i: int
    :param matches: list of matches in the current document
    :type matches: list
    """

    # call on the last match only
    if i != len(matches)-1:
        return

    # removing non-findings from the matches
    findings = [label == FINDING for _, label, _, _ in matches]
    for j, a_finding in zip(range(len(findings)-1, -1, -1), reversed(findings)):
        if not a_finding:
            matches.pop(j)

    doc.ents = matches


def get_entity_params(doc):
    """Produces the JSON representation of the entities.

    :param doc: spaCy doc object
    :type doc: spacy.tokens.doc.Doc
    """

    for ent in doc.ents:
        yield {
            'text': ent.text,
            'label': ent.label_,
            'start_token': ent.start,
            'end_token': ent.end,
            'start_char': ent.start_char,
            'end_char': ent.end_char
        }


class EntityMatcher:
    """An ``EntityMatcher`` object loads the `findings` from SNOMEDCT and uses
    them to identify symptoms in text. The ``match`` method extracts the
    entities (symptoms) from a string or a target URL.

    Code Example:

    >>> em = EntityMatcher()
    >>> em.load_snomedct()
    >>> em.match(text="A sentence with back pain.")
    >>> # [
    >>> #   {
    >>> #       'start_token': 3,
    >>> #       'end_char': 20,
    >>> #       'start_char': 16,
    >>> #       'end_token': 4,
    >>> #       'text': 'back',
    >>> #       'label': 'FINDING'
    >>> #   },
    >>> #   {
    >>> #       'start_token': 4,
    >>> #       'end_char': 25,
    >>> #       'start_char': 21,
    >>> #       'end_token': 5,
    >>> #       'text': 'pain',
    >>> #       'label': 'FINDING'
    >>> #   }
    >>> # ]
    """

    def __init__(self):

        self.nlp = spacy.load('en', tagger=None, parser=None, entity=None)
        self.matcher = Matcher(self.nlp.vocab)

    def load_snomedct(self):
        """Loads all SNOMEDCT term surface forms and their types into the
        spaCy matcher.

        """

        # We don't filter the loaded concepts here in order to 1. demonstrate
        # the callback function, and 2. allow the use of other types in the
        # future.
        for concept in SNOMEDCT.all_concepts_no_double():
            ctype = parse_ctype(concept.term).upper()
            patterns = self.load_concept_pattern(concept)
            key = str(concept.code)
            atts = {'code': concept.code, 'term': concept.term}

            self.matcher.add_entity(key, atts, on_match=ignore_non_findings)
            for token_specs in patterns:
                self.matcher.add_pattern(key, token_specs, label=ctype)

    def _orth(self, i):
        """Returns the orthographic representation of an item from the
        vocabulary based on an integer ID.

        :param i: string ID
        :type i: int
        :return: orthographic representation
        :rtype: str
        """

        return self.nlp.vocab[i].orth_

    def load_concept_pattern(self, concept):
        """Loads all surface forms of a concept as token patterns into the
        spaCy matcher.

        :param concept: SNOMEDCT concept
        :type concept: pymedtermino.snomedct.SNOMEDCTConcept
        """

        for t in concept.terms:

            # this is a big assumption; difficult to test though
            if not t.strip().endswith(')'):
                yield [{LOWER: tok.text.lower()} for tok in self.nlp(t)]

    def match(self, text=None, url=None):
        """Extracts SNOMEDCT `findings` from the target text or the text of the
        target URL.

        :param text: target text
        :type text: str
        :param url: target article URL
        :type url: str
        :return: spaCy document with entity matches
        :rtype: spacy.tokens.doc.Doc
        """
        if url is not None:
            text = scrape(url)

        if not text:
            raise ValueError('No target text or URL provided.')

        doc = self.nlp(text)
        self.matcher(doc)

        matches = list(get_entity_params(doc))

        return matches


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Symptom Recogniser based on '
                                                 'SNOMEDCT `findings`.')
    parser.add_argument('--text', dest='text', default=None,
                        help='Target text.')
    parser.add_argument('--url', dest='url', default=None,
                        help='The URL of target web page.')

    args = parser.parse_args()

    em = EntityMatcher()
    em.load_snomedct()

    try:
        ents = em.match(text=args.text, url=args.url)
        print(ents)
    except ValueError:
        args.help()
