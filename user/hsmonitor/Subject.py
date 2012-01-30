class Subject:
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def update(self, count=1):
        for o in self.observers:
            o.notify(count)