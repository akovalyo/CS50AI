import os
import random
import re
import sys
import copy
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


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
    # Create empty library for probability distribution with values = 0
    distrib = {x: 0.0 for x in corpus.keys()}
    total_pages = len(corpus)
    connect = set()
    # If page has connections, count probabilities and add to library
    if corpus[page]:
        for value in corpus[page]:
            connect.add(value)
        linked_prob = damping_factor / len(connect)
        for connect_page in connect:
            distrib[connect_page] += linked_prob
    # If page has no connections, all pages get equal probabilities
    else:
        for page in distrib.keys():
            distrib[page] = damping_factor / total_pages
    # Count additional probability for all pages
    all_probab = (1 - damping_factor) / total_pages
    for key in distrib:
        distrib[key] += all_probab
    return distrib


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create empty library for probability distribution with values = 0.0
    pagerank = {x: 0.0 for x in corpus.keys()}
    # Lib to calculate how many visits get the page
    page_visits = {x: 0 for x in corpus.keys()}
    # Randomly choose the first page
    next_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        distrib = transition_model(corpus, next_page, damping_factor)
        d_pages = list(distrib.keys())
        d_prob = list(distrib.values())
        # Randomly choose the next page according to calculated probabilities 
        next_page = np.random.choice(d_pages, p=d_prob)
        page_visits[next_page] += 1
    sum_visits = sum(page_visits.values())
    for page in page_visits.keys():
        pagerank[page] = page_visits[page] / sum_visits
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    all_prob = (1 - damping_factor) / total_pages
    # All pages get equal probabilities
    pagerank = {x: 1 / total_pages for x in corpus.keys()}
    check = True 
    # Loop while difference between the current rank values and the new 
    # rank values is > 0.001 
    while check:
        check = False
        pagerank_cp = copy.deepcopy(pagerank)
        # Iterate through all pages
        for page in pagerank.keys():
            # Remember previous page rank
            tmp_pr_page = pagerank[page]
            pagerank_cp[page] = all_prob
            # Iterate through all pages and calculate new PR for pages that have links
            # to tested page
            for page_i, link_i in corpus.items():
                if page in link_i:
                    pagerank_cp[page] += damping_factor * pagerank[page_i]/len(link_i)
                # A page that has no links interpreted as having one link 
                # for every page in the corpus, including itself
                elif not link_i:
                    pagerank_cp[page] += damping_factor * pagerank[page_i]/total_pages    
            # Check for difference between prevoius and current PR
            if abs(tmp_pr_page - pagerank_cp[page]) > 0.001:
                check = True
        # Update pageranks 
        for page in pagerank.keys():
            pagerank[page] = pagerank_cp[page]
    return pagerank        
            

if __name__ == "__main__":
    main()
