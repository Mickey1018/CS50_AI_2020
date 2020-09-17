import os
import copy
import random
import re
import sys
import math
import collections
import os
import copy
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

# The crawl function takes that directory, parses all of the HTML files in the directory,
# and returns a dictionary representing the corpus.
# The keys in that dictionary represent pages (e.g., "2.html"),
# and the values of the dictionary are a set of all of the pages linked to by the key (e.g. {"1.html", "3.html"}).

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    d = damping_factor
    n = len(corpus)

    # initialize a dictionary representing the probability distribution
    dict_prob = {}

    if corpus[page]:

        for pages in corpus:
            dict_prob[pages] = (1-d)/n

        for link in corpus[page]:
            dict_prob[link] += d/len(corpus[page])

    else:
        for pages in corpus:
            dict_prob[pages] = 1/n

    return dict_prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # to ensure n is at least equal to one
    if n < 1:
        raise Exception("Sorry, n should be at least 1")

    # randomly choose a first sample from the corpus of websites
    first_sample = random.choices(list(corpus.keys()), k=1)[0]

    # Initialize a list of sample result
    sample = []

    i = 0
    while i < n:

        # generate transition model with probability distribution
        model = transition_model(corpus, first_sample, damping_factor)

        next_page = []
        next_pagerank = []

        for key, val in model.items():

            # store page
            next_page.append(key)

            # store probability
            next_pagerank.append(val)

        # random pick one sample from corpus of webpages with known probability
        next_sample = random.choices(next_page, weights=next_pagerank, k=1)[0]

        # extract the first element from the resulting list
        sample.append(next_sample)

        first_sample = next_sample
        i += 1

    # to count the frequency of occurrence and transform to dictionary
    result = dict(collections.Counter(sample))

    # initialize the dictionary to store the normalized result
    norm_result = {}

    # normalization: convert count into proportion (or pagerank)
    for key, val in result.items():
        val = val / n
        norm_result[key] = val

    return norm_result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize a dictionary for storing pagerank
    pagerank = {}

    # abbreviation
    n = len(corpus)
    d = damping_factor

    # assign same pagerank to each page
    for pages in corpus:
        pagerank[pages] = 1 / n

    # initialize an update pagerank dictionary
    update_pagerank = {}

    # while the different between rank is not close enough
    diff_not_close = True
    while diff_not_close:

        # pick an page(p) from pagerank dictionary
        for page_p in pagerank:

            # initialize a score contributed by the previous page
            rank_by_prev_page = 0

            # pick an page(i) from corpus of webpages
            for page_i in corpus:

                # if page(i) link to page(p)
                if page_p in corpus[page_i]:
                    rank_by_prev_page += pagerank[page_i]/len(corpus[page_i])

                # if page(i) do not link to any pages, assume it links to all pages with same probability
                if not corpus[page_i]:
                    rank_by_prev_page += pagerank[page_i]/n

            # Iterative Algorithm
            update_pagerank[page_p] = (1-d)/n + d*rank_by_prev_page

        for page in pagerank:

            # compute if the previous pagerank and update pagerank are close enough to each other
            if not math.isclose(update_pagerank[page], pagerank[page], abs_tol=0.001):
                diff_not_close = True
            else:
                diff_not_close = False

            # go to the next page
            pagerank[page] = update_pagerank[page]

    return pagerank


if __name__ == "__main__":
    main()

# write an AI to carry out the task of page ranking
# For a corpus of web pages, AI ranks web pages by importance.
# 1. Sampling
# 2. Iterative Algorithm
# difference
