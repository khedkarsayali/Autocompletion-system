import tkinter as tk
from tkinter import Listbox
import re

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

class AutoCompleteApp:
    def __init__(self, root, trie):
        self.trie = trie
        self.root = root
        self.root.title("Autocomplete System")
        
        self.label = tk.Label(root, text="Enter text:")
        self.label.pack()
        
        self.textbox = tk.Text(root, height=5, width=50)
        self.textbox.pack()
        self.textbox.bind("<KeyRelease>", self.on_key_release)
        
        self.listbox = Listbox(root)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.insert_label = tk.Label(root, text="Insert a word:")
        self.insert_label.pack()

        self.insert_entry = tk.Entry(root)
        self.insert_entry.pack()

        self.insert_button = tk.Button(root, text="Insert", command=self.insert_word)
        self.insert_button.pack()

    def on_key_release(self, event):
        text = self.textbox.get("1.0", "end-1c").strip()  
        self.listbox.delete(0, tk.END)
        if text:
            # Split by spaces, semicolons, or newlines to find the last word
            words = re.split(r'[;\s\n\t]+', text)
            prefix = words[-1] if words else ""  # Take the last word as the prefix
            if prefix:
                suggestions = self.trie.autocomplete(prefix)
                for suggestion in suggestions:
                    self.listbox.insert(tk.END, suggestion)
    
    def on_select(self, event):
        if self.listbox.curselection():
            selected_text = self.listbox.get(self.listbox.curselection())
            current_text = self.textbox.get("1.0", "end-1c")
            words = re.split(r'([;\s\n]+)', current_text)
            if words:
                words[-1] = selected_text
                self.textbox.delete("1.0", "end")
                self.textbox.insert("1.0", "".join(words))

    def insert_word(self):
        word = self.insert_entry.get().strip()
        if word:
            self.trie.insert(word)
            self.insert_entry.delete(0, tk.END)
            print(f"Inserted word: {word}")

if __name__ == "__main__":
    trie = Trie()
    words = ['apple', 'app', 'apricot', 'ant', 'angel', 'bat', 'banana', 'book', 'car', 'cat', 'dog', 'door', 'elephant', 'doll', 'does']
    for word in words:
        trie.insert(word)
    
    root = tk.Tk()
    app = AutoCompleteApp(root, trie)
    root.mainloop()
