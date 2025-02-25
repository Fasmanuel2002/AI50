import os
import random
import re
import sys
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
        print(f"  {page}: {ranks}")


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

    #an be described as the probability that a random surfer is on that page at any given time
    #One way to interpret this model is as a Markov Chain, where each page represents a state
    #And each page has a transition model that chooses among its links at random. At each time step,
    # the state switches to one of the pages linked to by the current state.
    #To ensure we can always get to somewhere else in the corpus of web pages, we’ll introduce to our model a damping factor d.
    #Our random surfer now starts by choosing a page at random, and then, for each additional sample we’d like to generate, chooses a link from the current page at random with probability d, and chooses any page at random with probability 1 - d. If we keep track of how many times each page has shown up as a sample, we can treat the proportion of states that were on a given page as its 
    # PageRank
    #transition model debe devolverme la probabilidad de que una pagina sea esdcogida despeus de la pagina actual
def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    n = len(corpus.keys())
    random_prob = (1) / n

    probabilities = {p: random_prob for p in corpus}
    if corpus[page]:
        probab = damping_factor / len(corpus)
        for probab in corpus[page]:
            probabilities[probab] += random_prob
        
        else:
            for p in probabilities:
                probabilities[p] += damping_factor / (n - 1) 
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    
    #creemos samples
    visit_counts = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    
    
    
    for _ in range(n):
        transitional = transition_model(corpus, current_page, damping_factor)
        
        nextpage = random.choices(
            list(transitional.keys()),
            weights=(list(transitional.values())),
            k=n
        )[0]
        
        current_page = nextpage
        visit_counts[current_page] += 1
        
        pagerank = {page: count / (n - 1) for page, count in visit_counts.items()}
        
        
    return pagerank
        
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names
    """



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #Each page i that links to p has its own PageRank, 
    # PR(i)  representing the probability that we are on page i at any given time.
    
    N = len(corpus)
    data = []
    for pages, links in corpus.items():
        if links in corpus.values():
            num_links = int(len(links))
            m =  num_links
    Pri = np.ones(N) / N
    for _ in range(100):
        Pr = (1 - damping_factor) / N + damping_factor * (Pri / m)
        
    return Pr
    
  
if __name__ == "__main__":
    main()

