import nltk
import sys
import string

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
NP -> N | Det NP | Adj NP | NP PP
VP -> V | V NP | Adv VP | V PP | VP Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # call a set of alphabetic character
    alphabetic = set(string.ascii_letters)

    # convert the sentence is lower case first, and the tokenize it
    tokens = nltk.tokenize.word_tokenize(sentence.lower())

    # for each token, only get characters that are in the set of alphabetic character
    # remove token if none of it's character is in the set of alphabetic character
    for token in tokens:
        alphabet_chars = [char for char in token if char in alphabetic]
        if len(alphabet_chars) < 1:
            tokens.remove(token)

    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # initialize a list to store all noun phrase chunks
    np_chunks = []

    # get each possible noun phrase chunk and add it to the list
    for np_chunk in tree.subtrees(get_np_chunk):
        np_chunks.append(np_chunk)

    return np_chunks


def get_np_chunk(mytree):

    # condition 1: label is "NP"
    if mytree.label() == 'NP':

        # condition 2: does not itself contain any other noun phrases as subtrees
        if not list(mytree.subtrees(filter=lambda t: t.label() == 'NP' and t != mytree)):
            return True
    else:
        return False


if __name__ == "__main__":
    main()
