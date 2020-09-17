import nltk
import sys
import os
import string
import math

# welcome and encouraged to experiment with changing these values.
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        with open(path, 'r', encoding='utf8') as f:
            contents = f.read()
            files[file] = str(contents)
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by converting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punctuation = set(string.punctuation)
    stopwords = set(nltk.corpus.stopwords.words("english"))

    tokens = nltk.word_tokenize(document.lower())
    token = [token for token in tokens if token not in (punctuation | stopwords)]

    return token


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = dict()

    # get all the words from all the documents
    all_words = []
    for words in documents.values():
        for word in words:
            all_words.append(word)

    # calculate idf of each word
    total_document = len(documents.keys())
    for word in all_words:
        n_document = 0
        for document in documents.keys():
            try:
                if word in documents[document]:
                    n_document += 1
            except KeyError:
                n_document = 1

        idf = math.log(total_document / n_document)
        word_idf[word] = idf

    return word_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # compute tf-idf of each document
    document_score = dict.fromkeys([document for document in files.keys()], 0)
    for document in files.keys():
        for word in query:
            tf_idf = files[document].count(word) * idfs[word]
            document_score[document] += tf_idf

    sorted_document_score = sorted(document_score, key=lambda x: document_score[x], reverse=True)

    return sorted_document_score[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # initialize dictionaries to store idf value and
    # query term density of each sentence
    sentences_idf = dict.fromkeys([sentence for sentence in sentences.keys()], 0)
    sentences_qtd = dict.fromkeys([sentence for sentence in sentences.keys()], 0)

    # # compute the idf value and query term density for each sentence
    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                sentences_idf[sentence] += idfs[word]
                sentences_qtd[sentence] += sentences[sentence].count(word) / len(sentences[sentence])

    # sort by first, the idf value, second, the query term density
    sorted_sentences = sorted(sentences_idf,
                              key=lambda x: (sentences_idf[x], sentences_qtd[x]),
                              reverse=True)

    return sorted_sentences[0:n]


if __name__ == "__main__":
    main()
