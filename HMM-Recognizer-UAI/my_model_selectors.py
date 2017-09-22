import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        selected_model = None
        #Model selection: The lower the AIC/BIC value the better the model
        selected_score = float('inf')

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:

                model = self.base_model(num_states)
                logL = model.score(self.X, self.lengths)

                #calculate the score

                #p is the number of parameters
                #parameters = n * n + 2 * n * d - 1 where d is number of features
                p     = num_states * num_states + 2 * num_states * len(self.X[0]) - 1
                #N is the number of data points
                num_of_data = len(self.X)
                logN  = np.log(num_of_data)
                score = -2 * logL + p * logN

                if score < selected_score:
                    selected_model = model
                    selected_score = score

            except Exception:
                pass

        return selected_model



class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))

    Reference about DIC:
    https://www.mrc-bsu.cam.ac.uk/software/bugs/the-bugs-project-dic/

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        selected_model = None
        selected_score = float('-inf')

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:

                model = self.base_model(num_states)

                #log(P(original world))
                logL = model.score(self.X, self.lengths)

                #calculate mean of other words
                mean_other_words = 0
                same_word_count  = 0
                for word in self.words:
                    if word != self.this_word:
                        current_X, current_lengths = self.hwords[word]
                        mean_other_words += model.score(current_X, current_lengths)
                    else:
                        same_word_count+=1
                mean_other_words = mean_other_words / (len(self.words)-same_word_count)

                #cacuclate DIC
                #DIC = log(P(original world)) - average(log(P(otherwords)))
                score = logL - mean_other_words

                if score > selected_score:
                    selected_model = model
                    selected_score = score

            except Exception:
                pass

        return selected_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

        more about cross validation how it works:
        https://stats.stackexchange.com/questions/52274/how-to-choose-a-predictive-model-after-k-fold-cross-validation

    '''
    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        print("**test6")
        n_splits = min(len(self.lengths), 3)
        selected_model = None
        selected_score = float('-inf')
        split_method = KFold(n_splits)

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            model = self.base_model(num_states)
            score_total = 0
            iterations  = 0
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                try:
                    X_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                    X_test, lengths_test   = combine_sequences(cv_test_idx, self.sequences)

                    model.fit(X_train, lengths_train)
                    logL = model.score(X_test, lengths_test)
                    score_total += logL
                    iterations+=1
                except Exception:
                    pass

            if iterations > 0:
                mean_score = score_total/iterations
                if mean_score > selected_score:
                    selected_model = model
                    selected_score = mean_score

        return selected_model
