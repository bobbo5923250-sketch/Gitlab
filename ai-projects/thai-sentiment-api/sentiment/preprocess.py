"""Text normalisation and tokenisation for Thai.

Thai is written without spaces between words, so a word-level model needs a
dictionary-based tokenizer (PyThaiNLP's "newmm"). The function lives in its own
module so the trained pipeline can be pickled and loaded by the API.
"""

import re

from pythainlp.tokenize import word_tokenize

_URL = re.compile(r"https?://\S+")
_REPEAT = re.compile(r"(.)\1{2,}")  # "ดีมากกกกก" -> "ดีมากก"


def normalise(text: str) -> str:
    text = _URL.sub(" ", text.lower())
    return _REPEAT.sub(r"\1\1", text)


def thai_tokenize(text: str) -> list[str]:
    return [t for t in word_tokenize(normalise(text), engine="newmm") if t.strip()]
