from collections import defaultdict

from hashtags.text_utils import tokenize


def build_inverted_index(sentences_input_fn, filename):
    """ builds an inverted index in memory per document, with the word as key, pointing to the documents
    and sentences it appears at, as it uses my `tokenize` function, which removes punctuation and converts
    to lowercase, etc,
    @:param sentences_input_fn: function which generates sentences
    @:param filename: this document name """

    inv_index = defaultdict(list)
    for sentence in sentences_input_fn:
        for word in tokenize(sentence):
            inv_index[word].append((filename, sentence))
    return inv_index