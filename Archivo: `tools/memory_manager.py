class MemoryManager:
    def __init__(self, short_term_limit=10):
        self.short_term_memory = []
        self.long_term_memory = {}
        self.short_term_limit = short_term_limit

    def add_to_memory(self, key, value):
        if len(self.short_term_memory) >= self.short_term_limit:
            self.short_term_memory.pop(0)  # Eliminar el elemento más antiguo
        self.short_term_memory.append((key, value))
        self.long_term_memory[key] = value

    def get_from_memory(self, key):
        return self.long_term_memory.get(key, None)

    def clear_short_term_memory(self):
        self.short_term_memory = []
