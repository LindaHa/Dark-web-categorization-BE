import pickle
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences

from api.classification.labels import labels_index
from api.utils.singleton import Singleton

MAX_SEQUENCE_LENGTH = 1000


class Categorizer(metaclass=Singleton):
    def __init__(self):
        print('calling constructor')
        # Loading Tokenizer
        with open('models/tokenizer.pickle', 'rb') as handle:
            loaded_tokenizer = pickle.load(handle)
        # Loading saved Model

        import os
        cwd = os.getcwd()
        print(cwd)

        json_file = open('models/DarkWebCategoryModel.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # Loading saved Model Weights
        loaded_model.load_weights("models/DarkWebCategoryModel.h5")
        # Compiling loaded Model
        loaded_model.compile(loss='categorical_crossentropy',
                             optimizer='rmsprop',
                             metrics=['acc'])

        self.tokenizer = loaded_tokenizer
        self.model = loaded_model

    def categorize(self, content: str) -> str:
        sequences = self.tokenizer.texts_to_sequences([content])
        padded_seq = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
        predictions = self.model.predict(padded_seq)
        category_index = predictions[0].argmax(axis=0)
        category = labels_index[category_index]

        return category
