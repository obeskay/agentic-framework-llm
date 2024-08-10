import json
from typing import List, Any, Dict
from collections import deque

class MemoryManager:
    def __init__(self, stm_limit: int = 100, ltm_limit: int = 1000):
        self.short_term_memory: deque = deque(maxlen=stm_limit)
        self.long_term_memory: deque = deque(maxlen=ltm_limit)
        self.stm_limit = stm_limit
        self.ltm_limit = ltm_limit

    def add_to_stm(self, item: Any) -> None:
        self.short_term_memory.append(item)

    def add_to_ltm(self, item: Any) -> None:
        self.long_term_memory.append(item)

    def get_stm(self) -> List[Any]:
        return list(self.short_term_memory)

    def get_ltm(self) -> List[Any]:
        return list(self.long_term_memory)

    def save_session(self, filename: str) -> None:
        session_data = {
            "stm": list(self.short_term_memory),
            "ltm": list(self.long_term_memory)
        }
        with open(filename, 'w') as f:
            json.dump(session_data, f)

    def load_session(self, filename: str) -> None:
        with open(filename, 'r') as f:
            session_data = json.load(f)
        self.short_term_memory = deque(session_data["stm"], maxlen=self.stm_limit)
        self.long_term_memory = deque(session_data["ltm"], maxlen=self.ltm_limit)

    def search_memory(self, query: str) -> Dict[str, List[Any]]:
        stm_results = [item for item in self.short_term_memory if query.lower() in str(item).lower()]
        ltm_results = [item for item in self.long_term_memory if query.lower() in str(item).lower()]
        return {"stm": stm_results, "ltm": ltm_results}

    def clear_memory(self, memory_type: str = "all") -> None:
        if memory_type in ["all", "stm"]:
            self.short_term_memory.clear()
        if memory_type in ["all", "ltm"]:
            self.long_term_memory.clear()

    def transfer_stm_to_ltm(self, threshold: int) -> None:
        while len(self.short_term_memory) > threshold:
            item = self.short_term_memory.popleft()
            self.add_to_ltm(item)
