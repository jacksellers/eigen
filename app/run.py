from flask import Flask, render_template
from collections import Counter, OrderedDict
from glob import glob
from os import path
import nltk

app = Flask(__name__)
app.config['DEBUG'] = True
nltk.download('punkt')

# https://en.wikipedia.org/wiki/Most_common_words_in_English
COMMON_WORDS = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it',
    'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but',
    'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will',
    'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
    'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can',
    'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into',
    'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than',
    'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
    'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day',
    'most', 'us'
]

PUNCTUATION = ['.', ',', '!', '?', '-', ';', '"']

def get_words(doc):
    """Helper function to get the words from a text file."""
    # Turn the document into a list of lower case words
    with open(doc) as f:
        return [word.lower() for line in f for word in line.split()]

@app.route('/')
def index():
    """Main table page."""
    data = glob('app/data/*.txt')
    words = []
    for doc in data:
        words += get_words(doc)
    # Remove trailing punctuation
    words = [
        word[:-1] if word[-1] in PUNCTUATION
        else word for word in words
    ]
    # Remove common or blank words
    words = [
        word for word in words if word not in COMMON_WORDS and word != ''
    ]
    c = Counter(words)
    # Remove words that only appear once
    c = {x: count for x, count in c.items() if count > 1}
    od = OrderedDict(sorted(c.items(), key=lambda t: t[1], reverse=True))
    return render_template('index.html', od=od)

@app.route('/documents/<word>')
def documents(word):
    """Lists all of the documents containing a word."""
    data = glob('app/data/*.txt')
    docs = []
    for doc in data:
        words = set(get_words(doc))
        if word in words:
            head, tail = path.split(doc)
            docs.append(tail)
    return render_template('documents.html', word=word, docs=docs)

@app.route('/sentences/<word>')
def sentences(word):
    """Lists all of the sentences containing a word."""
    docs = glob('app/data/*.txt')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    all_sentences = []
    matches = []
    for doc in docs:
        f = open(doc)
        data = f.read()
        # Use the NLTK package to form sentences
        all_sentences += tokenizer.tokenize(data)
    for sentence in all_sentences:
        words = set([word.lower() for word in sentence.split()])
        if word in words:
            matches.append(sentence)
    return render_template('sentences.html', word=word, matches=matches)

app.run()