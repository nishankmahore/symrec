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
__author__ = 'Aleksandar Savkov'


FINDING = 104190
DISORDER = 209914


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


def keep_first_disorder(matcher, doc, i, matches):
    """A callback function that is called for all matches. Currently, it filters
    out all but the first `DISORDER` match, and assigns it the entities
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

    first_disorder = True
    j = 0

    sorted_matches = sorted(matches, key=lambda x: x[2])

    # removing non-disorder from the matches
    disorders = [label == DISORDER for _, label, _, _ in sorted_matches]
    for dis in disorders:
        if not dis or not first_disorder:
            matches.pop(j)
            continue

        first_disorder = False
        j += 1

    doc.ents = matches


def keep_matches(matcher, doc, i, matches):
    """A callback function that is called for all matches. Currently, it keeps
    all matched entities and passes them to the entities iterator.

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
    if i != len(matches) - 1:
        return

    doc.ents = matches