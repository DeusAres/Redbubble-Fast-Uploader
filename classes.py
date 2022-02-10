class Exit(Exception):
    pass

class stop:
    def __init__(self, s=False):
        self.s = s

    def set(self):
        self.s = False

    def clear(self):
        self.s = True

    def wait(self):
        if self.s:
            raise Exit("Stopped")

class index:
    def __init__(self, queue):
        self.s = 0
        self.update(queue)

    def update(self, queue):
        self.max = queue

    def add(self):
        self.s += 1
        if self.s >= self.max:
            raise Exit("All clear")

class entry:
    def __init__(self, file, preview=None):
        self.file = file
        self.preview = preview
    
    def updatePrev(self, preview, xy):
        self.preview = preview
        self.xy = xy