import re
import HTMLParser

import nltk

class KeywordExtractor:

    def __init__(self):
        self.html_parser = HTMLParser.HTMLParser()

        self.stop = nltk.corpus.stopwords.words("english")
        self.stop.append('rt')

        with open('contractions.txt', 'rb') as f:
            contractions = [c.strip().lower() for c in f.readlines()]

        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

        self.url_regex = re.compile(r"http[s]?[^\s]*")
        self.contractions_regex = re.compile("|".join(contractions))

        self.number_regex = re.compile(r'\b\d+\b')


    def extract(self, text):
        text = self.html_parser.unescape(text)
        text = text.lower()
        text = self.url_regex.sub('', text)
        text = self.contractions_regex.sub('', text)

        tokens = []
        for token in self.tokenizer.tokenize(text):
            if token not in self.stop and self.number_regex.search(token) is None:
                token = self.lemmatizer.lemmatize(token)
                tokens.append(token)

        return " ".join(tokens)
