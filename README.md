# symrec
A simplistic symptom recognition library based on 
[SNOMEDCT-CT](https://en.wikipedia.org/wiki/SNOMED_CT).

One of the most popular approaches to entity recognition is _term 
matching_. This application uses part of the terms in the _SNOMED-CT_
ontology to match entities in text.


### Installation

You will need to install 
[pymedtermino](https://pypi.python.org/pypi/PyMedTermino) and 
[spaCy](https://spacy.io/) (including the models) before you can install 
this package. After you have done so, you can install the package:

```
pip install git+https://github.com/savkov/symrec.git
```


### Usage

The library can be used both directly or as a `Flask` web service. To 
use the library in your code use the `EntityMatcher` object:

``` python
from symrec.matcher import EntityMatcher

text = """
The common symptoms of the disease are: high fever, night sweating,
joint pain, and fatigue. Some other less common ones are dizziness and
nausea.
"""

em = EntityMatcher()
em.load_snomedct()

em.match(text)
```

The `match` function returns a list of dictionaries, one for each match.

``` javascript
{
    "end_char": 55,
    "end_token": 11,
    "label": "FINDING",
    "start_char": 50,
    "start_token": 10,
    "text": "fever"
}
```

Alternatively, you can deploy the `Flask` service and access it through 
a `POST` request with an HTTP form:

```
python symrec/service.py
curl -X POST 'localhost:5000/symrec/text' -d "text=The common symptoms\ 
of the disease are: high fever, night sweating, joint pain, and \
fatigue. Some other less common ones are dizziness and nausea."
```

You can also specify a URL for `symrec` to scrape and extract entities 
from:

```
curl -X POST 'localhost:5000/symrec/url' -d \ 
"url=http://www.nhs.uk/Conditions/Heart-block/Pages/Symptoms.aspx" 
```

### Caveats

When loaded the library might require up to 7GB of memory. There are 
pending optimisations, but bear in mind that the library loads 500K+ 
terms into `spaCy`'s vocabulary. Even though `spaCy`'s matcher scales 
quite well, here we can see it strained quite a bit: processing a few 
paragraphs could take 10-15s.

### License

This library is release under GPLv3 license. You can find a copy as part
of the package in the LICENSE file.