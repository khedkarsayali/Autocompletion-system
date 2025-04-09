import tkinter as tk
from tkinter import ttk
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

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    self.insert(line.strip())
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Starting with an empty dictionary.")

    def save_to_file(self, filename):
        words = []
        self.collect_words(self.root, "", words)
        with open(filename, "w") as file:
            file.write("\n".join(words))

    def collect_words(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        for char, child in node.children.items():
            self.collect_words(child, prefix + char, words)

class AutoCompleteApp:
    def __init__(self, root):
        self.normal_trie = Trie()
        self.coding_trie = Trie()
        self.normal_file = "normal_dictionary.txt"
        self.coding_file = "coding_dictionary.txt"
        
        self.normal_trie.load_from_file(self.normal_file)
        self.coding_trie.load_from_file(self.coding_file)
        
        self.root = root
        self.root.title("Writing and Coding Assistant | Autocompletion System")
        self.root.geometry("500x450")
        
        self.mode = tk.StringVar(value="normal")
        self.theme = tk.StringVar(value="light")

        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = ttk.Label(self.main_frame, text="Enter text:")
        self.label.pack(anchor="w")
        
        self.textbox = tk.Text(self.main_frame, height=15, width=70, font=("Arial", 14))
        self.textbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.textbox.bind("<KeyRelease>", self.on_key_release)

        self.label = ttk.Label(self.main_frame, text="Suggestions:")
        self.label.pack(anchor="w")
        
        self.listbox = tk.Listbox(self.main_frame, height=8, font=("Arial", 14))
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        
        self.radio_frame = ttk.Frame(self.main_frame)
        self.radio_frame.pack(pady=5)
        
        self.normal_radio = ttk.Radiobutton(self.radio_frame, text="Normal Mode", variable=self.mode, value="normal", command=self.update_ui)
        self.coding_radio = ttk.Radiobutton(self.radio_frame, text="Coding Mode", variable=self.mode, value="coding", command=self.update_ui)
        self.inserting_radio = ttk.Radiobutton(self.radio_frame, text="Inserting Mode", variable=self.mode, value="inserting", command=self.update_ui)
        
        self.normal_radio.pack(side=tk.LEFT, padx=10)
        self.coding_radio.pack(side=tk.LEFT, padx=10)
        self.inserting_radio.pack(side=tk.LEFT, padx=10)
        
        self.insert_button_frame = ttk.Frame(self.main_frame)
        self.insert_normal_button = ttk.Button(self.insert_button_frame, text="Insert into Normal", command=self.insert_into_normal)
        self.insert_coding_button = ttk.Button(self.insert_button_frame, text="Insert into Coding", command=self.insert_into_coding)
        self.insert_normal_button.pack(side=tk.LEFT, padx=10)
        self.insert_coding_button.pack(side=tk.LEFT, padx=10)
        
        self.theme_button = ttk.Button(self.main_frame, text="Switch UI Mode", command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        self.clear_button = ttk.Button(self.main_frame, text="Clear", command=self.clear_textbox)
        self.clear_button.pack(pady=5)

    def update_ui(self):
        if self.mode.get() == "inserting":
            self.insert_button_frame.pack(pady=5)
        else:
            self.insert_button_frame.pack_forget()
    
    def on_key_release(self, event):
        text = self.textbox.get("1.0", "end-1c").strip()
        self.listbox.delete(0, tk.END)
        if text:
            words = re.split(r'[;\s\n\t]+', text)
            prefix = words[-1] if words else ""
            if prefix:
                suggestions = self.coding_trie.autocomplete(prefix) if self.mode.get() == "coding" else self.normal_trie.autocomplete(prefix)
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
    
    def insert_into_normal(self):
        word = self.textbox.get("1.0", "end-1c").strip()
        if word:
            self.normal_trie.insert(word)
            self.normal_trie.save_to_file(self.normal_file)
    
    def insert_into_coding(self):
        word = self.textbox.get("1.0", "end-1c").strip()
        if word:
            self.coding_trie.insert(word)
            self.coding_trie.save_to_file(self.coding_file)
    
    def toggle_theme(self):
        if self.theme.get() == "light":
            self.theme.set("dark")
            self.root.configure(bg="#2E2E2E")
            self.textbox.configure(bg="#1E1E1E", fg="white", insertbackground="white")  
            self.listbox.configure(bg="#1E1E1E", fg="white")
        else:
            self.theme.set("light")
            self.root.configure(bg="white")
            self.textbox.configure(bg="white", fg="black", insertbackground="black")  
            self.listbox.configure(bg="white", fg="black")

    
    def clear_textbox(self):
        self.textbox.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCompleteApp(root)
    root.mainloop()
