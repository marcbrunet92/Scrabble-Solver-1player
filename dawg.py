import pickle
"""
Ce fichier permet de construire un DAWG (Directed Acyclic Word Graph) à partir d'un lexique donné.
Il contient les fonctions nécessaires pour construire le DAWG, vérifier la validité d'un mot dans le DAWG,
et minimiser les nœuds du DAWG en utilisant un algorithme de minimisation.
"""

def build_trie(lexicon):
    """
    Function to build a trie from a given lexicon.
    :param lexicon: List of words to be added to the trie
    :return: The trie as a dictionary
    """

    num_nodes = 1
    trie = {0: {}}
    next_node = 1
    for word in lexicon:
        curr_node = 0
        for let in word:
            # if letter is present, move down its edge to next node
            if let in trie[curr_node]:
                edge_dict = trie[curr_node]
                curr_node = edge_dict[let]
            # otherwise, create new node and store its edge in current node
            # then move to it
            else:
                num_nodes += 1
                trie[next_node] = {}
                trie[curr_node][let] = next_node
                curr_node = next_node
                next_node += 1
        trie[curr_node]["END"] = True

    print(num_nodes)
    return trie


# function to check validity if word is in trie
def check_valid(word, trie):
    """
    Function to check if a word is valid in the trie.
    :param word: The word to be checked
    :param trie: The trie to be checked against
    :return: True if the word is valid, False otherwise"""
    curr_node = 0
    for letter in word:
        if letter in trie[curr_node]:
            curr_node = trie[curr_node][letter]
        else:
            return False
    if "END" in trie[curr_node]:
        return True
    else:
        return False

# Define a node to be stored in DAWG
class Node:
    """
    Class representing a node in the DAWG.
    Each node has a dictionary of children nodes and a boolean indicating if it is a terminal node.
    """
    next_id = 0

    def __init__(self):
        """
        Initialize a new node with an empty dictionary of children and set is_terminal to False.
        """
        self.is_terminal = False
        self.id = Node.next_id
        Node.next_id += 1
        self.children = {}

    def __str__(self):
        """
        String representation of the node, showing its ID and its children.
        :return: String representation of the node
        """
        out = [f"Node {self.id}\nChildren:\n"]
        letter_child_dict = self.children.items()
        for letter, child in letter_child_dict:
            out.append(f" {letter} -> {child.id}\n")
        return " ".join(out)

    def __repr__(self):
        """
        String representation of the node, showing its ID and whether it is terminal or not.
        :return: String representation of the node
        """
        out = []
        if self.is_terminal:
            out.append("1")
        else:
            out.append("0")
        for key, val in self.children.items():
            out.append(key)
            out.append(str(val.id))
        return "_".join(out)

    def __hash__(self):
        """
        Hash function for the node, using its string representation.
        :return: Hash value of the node
        """
        return self.__repr__().__hash__()

    def __eq__(self, other):
        """
        Equality function for the node, comparing their string representations.
        :param other: The other node to compare with
        :return: True if the nodes are equal, False otherwise"""
        return self.__repr__() == other.__repr__()


# returns length of common prefix
def length_common_prefix(prev_word, word):
    """
    Function to find the length of the common prefix between two words.
    :param prev_word: The previous word
    :param word: The current word
    :return: Length of the common prefix
    """
    shared_prefix_length = 0
    for letter1, letter2 in (zip(prev_word, word)):
        if letter1 == letter2:
            shared_prefix_length += 1
        else:
            return shared_prefix_length
    return shared_prefix_length


# minimization function
def minimize(curr_node, common_prefix_length, minimized_nodes, non_minimized_nodes):
    """
    Function to minimize the nodes in the DAWG.
    :param curr_node: The current node to be minimized
    :param common_prefix_length: Length of the common prefix
    :param minimized_nodes: Dictionary of minimized nodes
    :param non_minimized_nodes: List of non-minimized nodes
    :return: The current node after minimization
    """
    # Start at end of the non_minimized_node list. Then minimize nodes until lengths of
    # non_min_nodes and common_prefix are equal.
    for _ in range(len(non_minimized_nodes), common_prefix_length, -1):

        parent, letter, child = non_minimized_nodes.pop()

        if child in minimized_nodes:
            parent.children[letter] = minimized_nodes[child]

        else:
            minimized_nodes[child] = child

        curr_node = parent

    return curr_node


# function to build dawg from given lexicon
def build_dawg(lexicon):
    """
    Function to build a DAWG from a given lexicon.
    :param lexicon: List of words to be added to the DAWG
    :return: The root node of the DAWG
    """
    root = Node()
    minimized_nodes = {root: root}
    non_minimized_nodes = []
    curr_node = root
    prev_word = ""
    for i, word in enumerate(lexicon):
        # get common prefix of new word and previous word
        common_prefix_length = length_common_prefix(prev_word, word)

        # minimization step: only call minimize if there are nodes in non_minimized_nodes
        if non_minimized_nodes:
            curr_node = minimize(curr_node, common_prefix_length, minimized_nodes, non_minimized_nodes)

        # adding new nodes after the common prefix
        for letter in word[common_prefix_length:]:
            next_node = Node()
            curr_node.children[letter] = next_node
            non_minimized_nodes.append((curr_node, letter, next_node))
            curr_node = next_node

        # by the end of this process, curr_node should always be a terminal node
        curr_node.is_terminal = True
        prev_word = word
        # if i % 1000 == 0:
        #     print(i)

    minimize(curr_node, 0, minimized_nodes, non_minimized_nodes)
    print(len(minimized_nodes))
    return root


# check if word is in dawg
def find_in_dawg(word, curr_node):
    """
    Function to check if a word is valid in the DAWG.
    :param word: The word to be checked
    :param curr_node: The current node to be checked against
    :return: True if the word is valid, False otherwise
    """
    for letter in word:
        if letter in curr_node.children:
            curr_node = curr_node.children[letter]
        else:
            return False
    if curr_node.is_terminal:
        return True
    else:
        return False


if __name__ == "__main__":
    entry_path = input("Enter the path to the file whiwh contains all the word for a language (.txt): ")
    with open(entry_path, "r") as file:
        content = file.read()
    big_list = content.split()
    print(big_list[0:100])
    build_trie(big_list)
    root = build_dawg(big_list)

    languages = input("which languages do you want to save the DAWG for? (ex: fr, en)")
    save_path = f"languages/{languages}/{languages}.pickle"

    file_handler = open(save_path, "wb")
    pickle.dump(root, file_handler)
    file_handler.close()