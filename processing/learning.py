from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC

from .helpers import stop_words, get_data, merge_data, rand_reindex, reload_classifier, save_classifier


class SpottedAnalyzer(TransformerMixin):
    """Spotted Analyzer
    Analyzes and classifies spotteds using machine learning
    """

    def __init__(self, classifier='nb', detailed=False):
        self.classifier = classifier
        self.detailed = detailed

    def fit(self, X=None, y=None, reload=True):

        # Try to load a classifier
        if reload:
            loaded_classifier = reload_classifier(self.classifier, self.detailed)
        else:
            loaded_classifier = None

        # If the classifier was not loaded, fit the model
        if loaded_classifier is None:
            stopwords = stop_words()
            self.pipeline = Pipeline([
                ('vectorizer', CountVectorizer(strip_accents='ascii', analyzer='word', stop_words=stopwords, ngram_range=(1, 2))),
                ('tfidf', TfidfTransformer(use_idf=False)),
                ('classifier', MultinomialNB() if self.classifier == 'nb' else SVC(C=10, kernel='linear')),
            ])

            if not self.detailed and X is None:
                tmp = merge_data(get_data(), get_data(False))
                self.X = tmp['message']
                self.y = tmp['reason']
            elif X is None:
                tmp = rand_reindex(get_data(False, True))
                self.X = tmp['message']
                self.y = tmp['reason']
            else:
                self.X = X

            # Fit it
            self.pipeline.fit(self.X, self.y)

            # Save it
            save_classifier(self.pipeline, self.classifier, self.detailed)

        # If the classifier was loaded, save it
        else:
            self.pipeline = loaded_classifier

        return self

    def transform(self, X, prob=False):
        return self.pipeline.predict(X) if not prob else self.pipeline.predict_proba(X)


def spotted_analysis(spotted):
    results = SpottedAnalyzer().fit().transform([spotted], prob=True)

    if results[0][0] > 0.5:
        return True, 'Postar', results[0][0]

    else:
        return False, SpottedAnalyzer(detailed=True).fit().transform([spotted])[0], results[0][0]
