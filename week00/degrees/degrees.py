import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

num_explored = 0

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    while True:
        if input("Continue? (y/n) ") == "n":
            break
        source = person_id_for_name(input("Name (person 1): "))
        if source is None:
            print("Person not found.")
            continue
        target = person_id_for_name(input("Name (person 2): "))
        if target is None:
            print("Person not found.")
            continue

        start_time = time.time()
        path = shortest_path(source, target)

        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            print("\nNumber of states explored:", num_explored)
            print(f"Run time: {(time.time() - start_time):.2f} seconds\n")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    global num_explored
    
    # Initialize starting node and frontier
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    
    # initialize set for explored nodes
    explored = set()

    # Loop until solution found
    while True:
        # If nothing left in frontier, then there is no connection
        if frontier.empty():
            return None

        # Take the node from the frontier
        node = frontier.remove()
        num_explored += 1

        # Mark node as explored
        explored.add(node.get_state())

        # Add neighbors to the frontier
        for action, state in neighbors_for_person(node.get_state()):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state, node, action)
                frontier.add(child)
                # If the node is the target, then there is connection
                if child.get_state() == target:
                    connections = []
                    while child.get_parent() is not None:
                        connections.append((child.get_action(), child.get_state()))
                        child = child.get_parent()
                    connections.reverse()
                    return connections    

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()