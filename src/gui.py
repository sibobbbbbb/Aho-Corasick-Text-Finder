import tkinter as tk
from tkinter import filedialog, Text
import json
from aho_corasick import AhoCorasick

def load_file():
    file_path = filedialog.askopenfilename()
    process_file(file_path)

def process_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    text = data['text'].lower()
    patterns = [pattern.lower() for pattern in data['patterns']]
    ac = AhoCorasick(patterns)
    occurrences = ac.search(text)
    
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, data['text'])

    for tag in result_text.tag_names():
        result_text.tag_delete(tag)
    
    for pattern in patterns:
        if pattern in occurrences and occurrences[pattern]:
            result_text.insert(tk.END, f'\n\nPola "{pattern}" ditemukan {len(occurrences[pattern])}x.\n')
            for start, end in occurrences[pattern]:
                result_text.insert(tk.END, f"Indeks: [{start}, {end}]\n")
                
                # Highlighter
                start_idx = f"1.0 + {start} chars"
                end_idx = f"1.0 + {end + 1} chars"
                result_text.tag_add(pattern, start_idx, end_idx)
                result_text.tag_config(pattern, background="yellow", foreground="black")
        else:
            result_text.insert(tk.END, f'\n\nPola "{pattern}" ditemukan 0x.\n')


app = tk.Tk()
app.title("Aho-Corasick Text Finder")
app.geometry("600x500")

load_button = tk.Button(app, text="Load JSON File", command=load_file)
load_button.pack(pady=20)

result_text = Text(app, wrap='word',height=20,)
result_text.pack(pady=20)

app.mainloop()
