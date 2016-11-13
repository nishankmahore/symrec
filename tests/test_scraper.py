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
import pytest

from newspaper import ArticleException
from symrec.scraper import scrape

__author__ = 'Aleksandar Savkov'


def get_token_set(fp):

    return set(open(fp, 'r').read().replace('\n', ' ').split(' '))

# get the first three URLs
urls = open('../res/urls.txt', 'r').read().split('\n')[:3]

# load token sets representing the manually selected texts
articles = {url: get_token_set('../res/article{}.txt'.format(i))
            for i, url in enumerate(urls, start=1)}


def test_scraping_nhs():

    for url, tokens in articles.items():
        scraped_tokens = set(scrape(url).replace('\n', ' ').split(' '))
        assert not scraped_tokens - tokens, \
            'Scraped text does not match: {}'.format(url)


def invalid_url():

    scrape('invalid-url')


def test_invalid_url():

    with pytest.raises(ArticleException):
        invalid_url()
