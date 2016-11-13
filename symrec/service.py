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
from flask import request, Flask, jsonify
from newspaper import ArticleException

from symrec.matcher import EntityMatcher

__author__ = 'Aleksandar Savkov'


app = Flask(__name__)


# loading the term matcher and SNOMEDCT
matcher = EntityMatcher()
matcher.load_snomedct()


@app.route('/symrec/text', methods=['POST'])
def parse_text():
    """Processes the ``text`` parameter from the HTML form sent to
    ``/symrec/text`` and returns the extracted entities in JSON form.

    :return: JSON representation of extracted entities and attributes
    :rtype: flask.Response
    """

    text = request.form['text']
    entities = matcher.match(text=text)
    resp = jsonify(list(entities))
    resp.status_code = 200

    return resp


@app.route('/symrec/url', methods=['POST'])
def parse_url():
    """Scrapes the article text of a NHS disease article URL provided in the
    HTML form sent to ``/symrec/url``, and returns the extracted entities in
    JSON form.

    :return: JSON representation of extracted entities and attributes
    :rtype: flask.Response
    """

    try:
        url = request.form['url']
        entities = matcher.match(url=url)
        resp = jsonify(list(entities))
        resp.status_code = 200
        return resp
    except ArticleException as ex:
        msg = '{}: {}'.format(type(ex).__name__, str(ex))
        return error_handler(msg, 500)


def error_handler(error=None, status=None):
    """Handles server and request errors.

    :param error: error message
    :type error: str
    :param status: HTTP status
    :type status: int
    :return: error message
    :rtype: flask.Response
    """
    message = {
        'status': status,
        'message': 'Not Found: ' + request.url,
        'help': 'Use either `/symrec/text` for parsing text or `/symrec/url` '
                'for parsing a URL.',
        'error': str(error)
    }
    resp = jsonify(message)
    resp.status_code = status

    return resp


@app.errorhandler(404)
def not_found(error=None):
    """Handles 404 server errors.

    :param error: error message
    :type error: str
    """

    return error_handler(error, 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
