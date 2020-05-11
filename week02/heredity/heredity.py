import csv
import itertools
import sys

NAME = 'name'
MOTH = 'mother'
FATH = 'father'
TRAIT = 'trait'
GENE = 'gene'
MUT = 'mutation'

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def genes_from_parents(mother, father, one_gene, two_genes, num_genes):
    """
    Helper function for computing joint probability in person
    with parents
    """
    # Number of copies of gene person has
    genes_mother = 1 if mother in one_gene else 2 if mother in two_genes else 0
    genes_father = 1 if father in one_gene else 2 if father in two_genes else 0
    # Probability that child get gene from one parent
    prob_gene_mother = genes_mother / 2
    prob_gene_father = genes_father / 2
    # Compute probabilities according how many copies of gene child has
    if num_genes == 0:
        not_mother = (prob_gene_mother * PROBS[MUT] + (1 - prob_gene_mother) *
                      (1 - PROBS[MUT]))
        not_father = (prob_gene_father * PROBS[MUT] + (1 - prob_gene_father) *
                      (1 - PROBS[MUT]))               
        return not_mother * not_father

    elif num_genes == 1:
        not_mother = (prob_gene_mother * PROBS[MUT] + (1 - prob_gene_mother) *
                      (1 - PROBS[MUT]))
        from_mother = (prob_gene_mother * (1 - PROBS[MUT]) + (1 - prob_gene_mother) *
                       PROBS[MUT])
        not_father = (prob_gene_father * PROBS[MUT] + (1 - prob_gene_father) *
                      (1 - PROBS[MUT]))
        from_father = (prob_gene_father * (1 - PROBS[MUT]) + (1 - prob_gene_father) *
                       PROBS[MUT])
        return from_mother * not_father + from_father * not_mother
    
    elif num_genes == 2:
        from_mother = (prob_gene_mother * (1 - PROBS[MUT]) + (1 - prob_gene_mother) *
                       PROBS[MUT])
        from_father = (prob_gene_father * (1 - PROBS[MUT]) + (1 - prob_gene_father) *
                       PROBS[MUT])
        return from_mother * from_father
    
    return 0


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1.0
    # Iterate through all persons in people dictionary 
    for person in people.keys():
        prob_person = 1.0
        # Number of copies of gene person has
        num_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        # If person has parents, get probabilities from helper function
        if people[person][MOTH] and people[person][FATH]:
            prob_person = genes_from_parents(people[person][MOTH], people[person][FATH], one_gene, two_genes, num_genes)
            if person in have_trait: 
                prob_person *= PROBS[TRAIT][num_genes][True]
            else:
                prob_person *= PROBS[TRAIT][num_genes][False]     
        # If person doesn't have parents, calculate probabilities using
        # probability distribution
        else:    
            if num_genes == 0:
                prob_person *= PROBS[GENE][0]
                if person in have_trait: 
                    prob_person *= PROBS[TRAIT][0][True]
                else:
                    prob_person *= PROBS[TRAIT][0][False]
            elif num_genes == 1:
                prob_person *= PROBS[GENE][1]
                if person in have_trait: 
                    prob_person *= PROBS[TRAIT][1][True]
                else:
                    prob_person *= PROBS[TRAIT][1][False]
            elif num_genes == 2:
                prob_person *= PROBS[GENE][2]
                if person in have_trait: 
                    prob_person *= PROBS[TRAIT][2][True]
                else:
                    prob_person *= PROBS[TRAIT][2][False]
        probability *= prob_person    
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if person in one_gene:
            probabilities[person][GENE][1] += p
        elif person in two_genes:
            probabilities[person][GENE][2] += p
        else:
            probabilities[person][GENE][0] += p
        if person in have_trait:
            probabilities[person][TRAIT][True] += p
        else:
            probabilities[person][TRAIT][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        divider = 0.0
        for i in range(3):
            divider += probabilities[person][GENE][i]
        for i in range(3):
            probabilities[person][GENE][i] = probabilities[person][GENE][i] / divider
        
        divider = 0.0
        for item in [True, False]:
            divider += probabilities[person][TRAIT][item]
        for item in [True, False]:
            probabilities[person][TRAIT][item] = probabilities[person][TRAIT][item] / divider


if __name__ == "__main__":
    main()