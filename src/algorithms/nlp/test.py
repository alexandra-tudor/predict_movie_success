import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

from src.algorithms.nlp.glove_word2vec import MeanEmbeddingVectorizer, TfidfEmbeddingVectorizer

import gensim


# let X be a list of tokenized texts (i.e. list of lists of tokens)

df = pd.read_csv('../../../data/compressed_dataset.csv', sep='\t')
texts = df['Plot'].tolist()

texts = map(lambda l: l.split(), texts)

model = gensim.models.KeyedVectors.load_word2vec_format(texts)
w2v = dict(zip(model.index2word, model.syn0))

etree_w2v = Pipeline([
    ("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)),
    ("extra trees", ExtraTreesClassifier(n_estimators=200))])
etree_w2v_tfidf = Pipeline([
    ("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),
    ("extra trees", ExtraTreesClassifier(n_estimators=200))])