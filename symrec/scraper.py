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
from newspaper import Article

__author__ = 'Aleksandar Savkov'


def scrape(url):
    """Scrapes an article from a web page and returns its text without
    boilerplate.

    :param url: article URL
    :type url: str
    :return: article text
    :rtype: str
    """

    a = Article(url)
    a.download()
    a.parse()

    return a.text

