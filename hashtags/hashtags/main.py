from hashtags.index import build_inverted_index
from hashtags.io import read_files
from hashtags.text_utils import calculate_fdist, sentences
from collections import defaultdict


def _merge_indexes(inv_idx, new_inv_idx):
    """ merges two dicts, adding the values when the keys are the same """
    for key, value in new_inv_idx.items():
        if key in inv_idx:
            inv_idx[key] = inv_idx[key] + value
        else:
            inv_idx[key] = value


def print_hashtags(file_path, num_common_words=10):
    """ main method which reads the text files in a folder and builds an inverted index in memory,
    then with the loaded text gets the num_common_words most common words and prints them with the
    document and sentence they occur at

    @:param file_path: folder containing the text files
    @:param num_common_words
    """
    all_text = ""
    inv_idx = defaultdict(list)
    for (filename, text) in read_files(file_path):
        sentences_fn = sentences(text)
        new_inv_idx = build_inverted_index(sentences_fn, filename)
        _merge_indexes(inv_idx, new_inv_idx)
        all_text += " " + text
    fdist = calculate_fdist(all_text)
    for word, frequency in fdist.most_common(num_common_words):
        print(u'{} {}'.format(word, frequency))
        print('')
        for (doc, sentence) in inv_idx[word]:
            print(u'{}: {}'.format(doc, sentence))
        print('------------------------------')


print_hashtags('../testdocs')
