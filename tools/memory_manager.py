class MemoryManager:
    def __init__(self, stm_limit=100, ltm_limit=1000):
        self.short_term_memory = []
        self.long_term_memory = []
        self.stm_limit = stm_limit
        self.ltm_limit = ltm_limit

    def add_to_stm(self, item):
        self.short_term_memory.append(item)
        if len(self.short_term_memory) > self.stm_limit:
            self.short_term_memory.pop(0)

    def add_to_ltm(self, item):
        self.long_term_memory.append(item)
        if len(self.long_term_memory) > self.ltm_limit:
            self.long_term_memory.pop(0)

    def get_stm(self):
        return self.short_term_memory

    def get_ltm(self):
        return self.long_term_memory

    def save_session(self, filename):
        # Implementation for saving session
        pass

    def load_session(self, filename):
        # Implementation for loading session
        pass
