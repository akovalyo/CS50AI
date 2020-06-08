import nltk
import sys
import os
import math
from collections import Counter

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
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files_dict = {}
    for file in files:
        with open(os.path.join(directory, file), mode="r") as f:
            content = f.read()
            files_dict[file] = content
    return files_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    w_list = [word for word in nltk.word_tokenize(document.lower()) if word.isalpha() and not word in stopwords]
    return w_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Number of documents in corpus
    n_doc = len(documents)
    counted_all = Counter()

    # Iterate through every document and map appearence of all words in the document and
    # for every word count in how many documents it is present
    for doc in documents.values():
        counted = {word: 1 for word in doc}
        counted_all += Counter(counted)
    idf_dict = dict(counted_all)

    # Calculate the IDF value of the word
    for key, value in idf_dict.items():
        idf_dict[key] = math.log(n_doc / value)

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    words = {word: [] for word in query}
    # For every word in the query calculate the sum of tfidf values for every file
    for word in query:
        for doc, value in files.items():
            counted = Counter(value)
            if word in counted:
                amount_word = counted[word]
            else:
                amount_word = 0
            words[word].append((amount_word * idfs[word], doc))
    # Calculate total tfidf for evert file
    docs = {doc: 0 for doc in files.keys()}
    for word, value in words.items():
        for doc in value:
            docs[doc[1]] += doc[0]
    docs_sorted = [name for name, value in sorted(docs.items(), key=lambda item: -item[1])]
    
    return docs_sorted[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sents = {}
    
    for sentence in sentences:
        w_in_sent = 0
        sent_idf = 0
        excl = 1
        # Exclude titles from the results
        if '==' in sentence:
            excl = 0
        for word in query:    
            if word in sentences[sentence]:
                w_in_sent += 1
                sent_idf += idfs[word] * excl
                sents[sentence] = (sent_idf, w_in_sent / len(sentences[sentence]))
    sent_sorted = [sent for sent, value in sorted(sents.items(), key=lambda item: (-item[1][0], -item[1][1]))]
    return sent_sorted[:n]


if __name__ == "__main__":
    main()
