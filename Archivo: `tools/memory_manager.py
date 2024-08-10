class MemoryManager:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = {}

    def add_to_memory(self, key, value):
        self.long_term_memory[key] = value

    def get_from_memory(self, key):
        return self.long_term_memory.get(key, None)
