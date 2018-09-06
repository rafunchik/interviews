from unittest import TestCase

from hashtags.text_utils import tokenize


class TestTokenize(TestCase):

    def test_tokenize_no_stopwords(self):
        text = "remove me"
        self.assertEquals(tokenize(text), ['remove'])

    def test_tokenize_lowers_case(self):
        text = "CraZy caSe"
        self.assertEquals(tokenize(text), ['crazy', 'case'])

    def test_tokenize_remove_punctuation(self):
        text = "rafa's the: story... tomorrow :"
        self.assertEquals(tokenize(text), ['rafa', 'story', 'tomorrow'])

    def test_tokenize_remove_numbers(self):
        text = "2334 three"
        self.assertEquals(tokenize(text), ['three'])

    def test_tokenize_empty_doc(self):
        text = "  "
        self.assertEquals(tokenize(text), [])

    def test_tokenize_doc_remove_len_1(self):
        text = " just a sanity check a 1"
        self.assertEquals(tokenize(text), ['sanity', 'check'])
