class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix):
        node = self.search(prefix)
        if not node:
            return []
        
        results = []
        self.dfs(node, prefix, results)
        return results

    def dfs(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            self.dfs(child_node, prefix + char, results)


trie = Trie()
words = [
    'apple', 'app', 'apricot', 'ant', 'angel',
    'bat', 'ball', 'banana', 'book', 'bottle',
    'car', 'cat', 'chair', 'camera', 'coep',
    'dog', 'drum', 'dance', 'door', 'desk',
    'elephant', 'eagle', 'engine', 'echo', 'earth',
    'fish', 'fire', 'forest', 'flower', 'flag',
    'game', 'guitar', 'garden', 'glass', 'gate',
    'house', 'hammer', 'horse', 'hill', 'honey',
    'island', 'ice', 'iron', 'ink', 'ivory',
    'jacket', 'jam', 'jungle', 'jump', 'jewel',
    'kite', 'king', 'key', 'kitten', 'kitchen',
    'lion', 'lamp', 'lake', 'leaf', 'ladder',
    'mountain', 'moon', 'mirror', 'magnet', 'mouse',
    'night', 'nest', 'net', 'nurse', 'notebook',
    'orange', 'ocean', 'owl', 'onion', 'octopus',
    'pencil', 'paper', 'plane', 'plate', 'pillow',
    'queen', 'quilt', 'quiz', 'quiver', 'quest',
    'rabbit', 'rainbow', 'river', 'rocket', 'rose',
    'sun', 'star', 'stone', 'snake', 'spoon',
    'tree', 'table', 'train', 'tiger', 'tower',
    'umbrella', 'uniform', 'unicorn', 'universe', 'urge',
    'van', 'vase', 'violet', 'volcano', 'victory',
    'water', 'window', 'wall', 'whale', 'watch',
    'xylophone', 'xenon', 'xerox', 'xylograph', 'xiphoid',
    'yellow', 'yacht', 'yawn', 'yarn', 'year',
    'zebra', 'zero', 'zone', 'zoom', 'zinc'
]

for word in words:
    trie.insert(word)


while True:
    prefix = input("Enter prefix to autocomplete or exit ").strip()
    if prefix.lower() == 'exit':
        break
    results = trie.autocomplete(prefix)
    if results:
        print("Autcompletion results :", results)
    else:
        print("No suggestions found.")

