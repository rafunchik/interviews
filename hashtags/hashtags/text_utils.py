import nltk


def calculate_fdist(text):
    """ calculates words frequency distribution in a text
    :param text:
    :return: type: nltk.FreqDist
    """
    words = tokenize(text)
    return nltk.FreqDist(words)


def tokenize(text, language='english'):
    """
    custom tokenizer, tokenizes a text, removing the provided language's stopwords and punctuation, converting to
    lowercase, and checking whether the resulting word is alphanumeric and with length more than 1. No stemming.

    :param text:
    :param language: defaults to English
    :return: tokenized words
    """
    stop_words = set(nltk.corpus.stopwords.words(language))
    words = nltk.word_tokenize(text, language)
    words = [word.lower() for word in words if _word_is_valid(word.lower(), stop_words)]
    return words


def _word_is_valid(word, stop_words):
    return (len(word) > 1) and (word not in stop_words) and word.isalpha()


def sentences(text, language='english'):
    """ tokenize in sentences using NTLK, defaults to English language (therefore English's punctuation, etc.) """
    return nltk.sent_tokenize(text, language)
