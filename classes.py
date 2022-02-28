import drawerFunctions as df
import os
from pathlib import Path

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

class queue:
    def __init__(self):
        self.entries = []
        self.currentIndex = 0
        self.maxIndex = 0

    def append(self, entry):
        self.entries.append(entry)
        self.maxIndex += 1

    def pop(self, index):
        self.entries.pop(index)
        self.maxIndex -= 1
        if self.currentIndex >= index:
            self.currentIndex -= 1

    def popMultiple(self, indexes):
        self.entries = [self.entries[i] 
            for i in range(len(self.entries))
            if i not in indexes
        ]
        
        for i in indexes:
            if self.currentIndex >= i:
                self.currentIndex -= 1

        self.maxIndex -= self.len()


    def getCurrentFile(self):
        return self.entries[self.currentIndex]

    def __getitem__(self, key):
        return self.entries[key]

    def len(self):
        return len(self.entries)

    def next(self):
        self.currentIndex += 1
        if self.currentIndex >= self.maxIndex:
            raise Exit("All clear")
        
    def updateStatus(self, status):
        self.entries[self.currentIndex].updateStatus(status)

    def displayListbox(self):
        return [each.displayListbox() for each in self.entries]

    def displayUpload(self):
        return [each.displayUpload() for each in self.entries]

class entry:
    def __init__(self, file, preview=None):
        self.file = file
        self.filename = Path(file).name
        self.preview = preview
        self.pin = False
        self.title = None
        self.tags = None
        self.desc = None
        self.background = None
        self.products = None

    def updatePreview(self, preview, xy):
        self.preview = preview
        self.xy = xy

    def addData(self, title, tags, desc, types, background, products):
        self.title = title
        self.tags = tags
        self.desc = desc
        self.background = background
        self.products = products

        self.images = {
            'normal' : self.file,
            'rotated' : None,
            'sticker' : None,
            'rotatedSticker' : None,
            'squared' : None,
        }

        for each in types:
            self.images[each] = True 

        self.status = 'Pending'

    def addPin(self, board, section):
        self.pin = True
        self.board = board
        self.section = section

    def updateStatus(self, status):
        self.status = status

    def displayListbox(self):
        return self.filename
    
    def displayUpload(self):
        return [str(each) for each in [
                        self.filename, 
                        self.title,
                        self.tags,
                        self.desc,
                        self.background,
                        list(self.images.keys()),
                        self.products,
                        self.status
                    ]
                ]

    def makeVariations(self):
        temp = df.openImage(self.images['normal'])[0].convert("RGBA")
        # saving the path
        path = os.getcwd()
        for each in self.images.keys():
            if each != 'normal' and self.images[each]:
                self.images[each] = f'{path}\\{each}.png'
                temp2 = None
                # creating the images
                if each == 'rotated':
                    temp2 = df.rotate(temp, -90)[0]
                    
                elif each == 'sticker':
                    temp2 = df.strokeImage(temp, 4, self.background)

                elif each == 'rotatedSticker':
                    temp2 = df.rotate(df.strokeImage(temp, 4, self.background), -90)[0]

                elif each == 'squared':
                    temp3 = df.cropToRealSize(temp)[0]
                    exp = int(min(temp.size) * 30 / 100)
                    temp2 = df.backgroundPNG(*[each + exp for each in temp3.size], self.background)[0]
                    temp2 = df.pasteItem(temp2, temp3, *[temp2.size[i]//2-temp3.size[i]//2 for i in range(2)])

                if temp2 != None:
                    temp2.save(f'{path}\\{each}.png', optimize=True)
            
    def makePin(self):
        image = df.openImage(self.images['normal'])[0]
        background = df.backgroundPNG(1000, 1500, self.background)[0]
        image = df.resizeToFitSpace(image, [each*0.95 for each in background.size])[0]
        background = df.pasteItem(background, image, *df.centerItem(background, image)).convert('RGB')
        path = os.getcwd() + "\\" + "pin.jpg"
        background.save(path, optimize=True)
        self.social = path

    def delete(self):
        # removing all the images excluding normal
        for each in list(self.images.values())[1:]:
            if each is not None:
                try:
                    os.remove(each)
                except:
                    print(f"Couldn't remove {each}")