from unittest import TestCase

from hashtags.index import build_inverted_index


def _generate_index(text_list, docname):
    sentence_fn = (sentence for sentence in text_list)
    return build_inverted_index(sentence_fn, docname)


class TestBuildInvertedIndex(TestCase):

    def test_build_inverted_index_word_in_two_sentences_case_insensitive(self):
        text_list = ["hey Eigen tech!", "`eigen values` are cool", "something else"]
        new_inv_idx = _generate_index(text_list, "test1")
        self.assertEqual(new_inv_idx['eigen'], [("test1", 'hey Eigen tech!'), ("test1", '`eigen values` are cool')])

    def test_build_inverted_index_keys_are_lowercase(self):
        text_list = ["hey Eigen tech!", "`eigen values` are cool", "something else"]
        new_inv_idx = _generate_index(text_list, "test1")
        self.assertEqual(new_inv_idx['EIGEN'], [])

    def test_word_not_in_build_inverted_index_returns_empty_list(self):
        text_list = ["something else"]
        new_inv_idx = _generate_index(text_list, "test1")
        self.assertEqual(new_inv_idx['word_not_in_vocabulary'], [])

    def test_build_inverted_index_empty_filelist_empty_index(self):
        text_list = []
        new_inv_idx = _generate_index(text_list, "test1")
        self.assertEqual(new_inv_idx['word_not_in_vocabulary'], [])
