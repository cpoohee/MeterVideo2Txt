import pytest
from src.WordMatch import WordMatch

def test_initialise():
    wordmatch = WordMatch()

def test_word_embedding():
    wordmatch = WordMatch()
    word1 = 'word1'
    word2 = 'word2'
    emb1 = wordmatch.word_embedding(word1)
    emb2 = wordmatch.word_embedding(word2)

    assert emb1 != pytest.approx(emb2)

def test_word_similarity1():
    wordmatch = WordMatch()
    word1 = 'word1'
    word2 = 'word2'
    emb1 = wordmatch.word_embedding(word1)
    emb2 = wordmatch.word_embedding(word2)
    cos1 = wordmatch.cosine_similarity(emb1, emb1)

    assert cos1 == pytest.approx(1.0000)

    cos2 = wordmatch.cosine_similarity(emb1, emb2)

    assert cos2 != pytest.approx(1.0000)

def test_word_similarity2():
    wordmatch = WordMatch()

    emb1 = wordmatch.word_embedding('sp02')
    emb2 = wordmatch.word_embedding('sp0z')
    emb3 = wordmatch.word_embedding('spO2')
    emb4 = wordmatch.word_embedding('PRbpm')

    cos1 = wordmatch.cosine_similarity(emb1, emb1)
    cos2 = wordmatch.cosine_similarity(emb1, emb2)
    cos3 = wordmatch.cosine_similarity(emb1, emb3)
    cos4 = wordmatch.cosine_similarity(emb1, emb4)

    assert cos1 == pytest.approx(1.0000)
    assert cos1 > cos4
    assert cos2 > cos4
    assert cos3 > cos4

def test_word_matching():
    word_match = WordMatch()
    word_match.add_keyword('sp02')
    word_match.add_keyword('PRbpm')

    assert 'sp02' == word_match.match_to_keyword('spO2')
    assert 'PRbpm' == word_match.match_to_keyword('bpm')