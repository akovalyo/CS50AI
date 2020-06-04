# Project 2a: PageRank

Write an AI (PageRank algorithm) to rank web pages by importance.

## Background
<details>
	<summary>Read</summary>

    When search engines like Google display search results, they do so by
    placing more “important” and higher-quality pages higher in the search
    results than less important pages. But how does the search engine know
    which pages are more important than other pages?

    One heuristic might be that an “important” page is one that many other
    pages link to, since it’s reasonable to imagine that more sites will link
    to a higher-quality webpage than a lower-quality webpage. We could
    therefore imagine a system where each page is given a rank according to
    the number of incoming links it has from other pages, and higher ranks
    would signal higher importance.

    But this definition isn’t perfect: if someone wants to make their page
    seem more important, then under this system, they could simply create
    many other pages that link to their desired page to artificially inflate
    its rank.

    For that reason, the PageRank algorithm was created by Google’s
    co-founders (including Larry Page, for whom the algorithm was named). In
    PageRank’s algorithm, a website is more important if it is linked to by
    other important websites, and links from less important websites have
    their links weighted less. This definition seems a bit circular, but it
    turns out that there are multiple strategies for calculating these rankings.

</details>

## Description

Implement 2 approaches for calculating PageRank – calculating both by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula. 

**Random Surfer Model**

One approach is to use hypothetical surfer on the internet who clicks on links at random. It starts with a web page at random, and then randomly chooses links to follow. A page’s PageRank, then, can be described as the probability that a random surfer is on that page at any given time. After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page. Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.

By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank. We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page. After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page might be an estimate for that page’s rank.

To ensure surfer can always get to somewhere else in the corpus of web pages, algorithm has a damping factor d. With probability d (where d is usually set around 0.85), the random surfer will choose from one of the links on the current page at random. But otherwise (with probability 1 - d), the random surfer chooses one out of all of the pages in the corpus at random (including the one they are currently on).

**Iterative Algorithm**

Another approach is to define a page’s PageRank using a recursive mathematical expression.

PageRank for a page p:

![formula](https://github.com/akovalyo/CS50AI/blob/master/week02/pagerank/src/formula.png?raw=true)

**d** is the damping factor, **N** is the total number of pages in the corpus, **i** ranges over all pages that link to page **p**, and **NumLinks(i)** is the number of links present on page **i**.

___

## Algorithm in action

**Requirements:**

* numpy

**Usage:**

```bash
python pagerank.py [DIRECTORY]
```

DIRECTORY - the name of a directory of a corpus of web pages to compute PageRanks for. 

**Output:**

* PageRank Results from Sampling - page name and PageRank (a number between 0 and 1). The values in probability distribution should sum to 1.

* PageRank Results from Iteration - page name and PageRank (a number between 0 and 1). The values in probability distribution should sum to 1.

The output of these two algorithms should be similar when given the same corpus.

*Video on youtube showing result*

[![PageRank - youtube](https://img.youtube.com/vi/2pqBiKSvcQc/0.jpg)](https://youtu.be/2pqBiKSvcQc)