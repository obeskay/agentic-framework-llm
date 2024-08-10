import threading

class AsyncAgent:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        thread = threading.Thread(target=task)
        self.tasks.append(thread)
        thread.start()

    def wait_for_tasks(self):
        for task in self.tasks:
            task.join()
