from gensim.models import word2vec
import json

# Settings
seed = 666
sg = 0      # 0 for CBOW, 1 for skip-gram
window_size = 10
vector_size = 100
min_count = 1
workers = 8
epochs = 5
batch_words = 10000

def train_model(filepath, algorithm, model_name):
    train_data = word2vec.LineSentence(filepath)
    model = word2vec.Word2Vec(
        train_data,
        min_count=min_count,
        vector_size=vector_size,
        workers=workers,
        epochs=epochs,
        window=window_size,
        sg=algorithm,
        seed=seed,
        batch_words=batch_words
    )
    model.save(model_name)

path1 = 'data/pubmed_data_1000.txt'
path2 = 'data/pubmed_data_5000.txt'
path3 = 'data/pubmed_data_10000.txt'

train_model(path1, 0, 'model/cbow_1000.model')
train_model(path1, 1, 'model/skipgram_1000.model')
train_model(path2, 0, 'model/cbow_5000.model')
train_model(path2, 1, 'model/skipgram_5000.model')
train_model(path3, 0, 'model/cbow_10000.model')
train_model(path3, 1, 'model/skipgram_10000.model')
