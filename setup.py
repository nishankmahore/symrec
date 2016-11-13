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
from setuptools import setup, find_packages

__author__ = 'Aleksandar Savkov'

setup(
    name='symrec',
    version='0.1',
    description='A baseline symptom recognition web service',
    author='Aleksandar Savkov',
    author_email='aleksandar@savkov.eu',
    url='https://github.com/savkov/symrec',
    packages=find_packages(),
    install_requires=['spacy', 'flask', 'pymedtermino', 'newspaper3k',
                      'flask-restful'],
    license='GPLv3',
    platforms=['Unix', 'MacOS']
)
