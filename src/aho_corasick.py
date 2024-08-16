from collections import deque, defaultdict

class AhoCorasick:
    def __init__(self, patterns):
        self.trie = {}
        self.output = defaultdict(list)
        self.fail = {}
        self.build_trie(patterns)
        self.build_fail_links()

    def build_trie(self, patterns):
        new_state = 0
        for pattern in patterns:
            current_state = 0
            for char in pattern:
                if current_state not in self.trie:
                    self.trie[current_state] = {}
                if char not in self.trie[current_state]:
                    new_state += 1
                    self.trie[current_state][char] = new_state
                current_state = self.trie[current_state][char]
            self.output[current_state].append(pattern)

    def build_fail_links(self):
        queue = deque()
        for char in self.trie[0]:
            state = self.trie[0][char]
            queue.append(state)
            self.fail[state] = 0

        while queue:
            r = queue.popleft()
            for char, u in self.trie.get(r, {}).items():
                queue.append(u)
                state = self.fail[r]
                while state and char not in self.trie.get(state, {}):
                    state = self.fail[state]
                self.fail[u] = self.trie[state].get(char, 0) if state in self.trie and char in self.trie[state] else 0
                self.output[u].extend(self.output[self.fail[u]])

    def search(self, text):
        state = 0
        occurrences = defaultdict(list)
        for i, char in enumerate(text):
            while state and char not in self.trie.get(state, {}):
                state = self.fail.get(state, 0)
            state = self.trie[state].get(char, 0)
            for pattern in self.output.get(state, []):
                start_index = i - len(pattern) + 1
                occurrences[pattern].append((start_index, i))
        return occurrences