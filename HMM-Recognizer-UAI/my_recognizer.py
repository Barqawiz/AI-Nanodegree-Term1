import warnings
import operator
from asl_data import SinglesData

#reference how to solve: question in the forum: https://discussions.udacity.com/t/recognizer-implementation/234793/2
#reference how to find the max: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]

   """

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    index = 0
    for X, lengths in test_set.get_all_Xlengths().values():
        probabilities.insert(index, dict())
        for word, model in models.items():
            try:
                score = model.score(X, lengths)
                probabilities[index][word] = score
            except:
                probabilities[index][word] = float("-inf")


        guesses.append(max(probabilities[index].items(), key=operator.itemgetter(1))[0])
        index += 1




    return probabilities, guesses
