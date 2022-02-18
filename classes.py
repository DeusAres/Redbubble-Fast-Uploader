import drawerFunctions as df
import os

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


class fileObj:
    def __init__(self, image, title, tags, desc, types, background):
        self.title = title
        self.tags = tags
        self.desc = desc
        self.images = {
            'normal' : image,
            'rotated' : None,
            'sticker' : None,
            'rotatedSticker' : None,
            'squared' : None,
        }
        self.background = background

        temp = df.openImage(image)[0].convert("RGBA")
        for each in types:
            path = os.getcwd()
            # saving the path
            if each in self.images.keys() and each != 'normal':
                self.images[each] = f'{path}\\{each}.png'
                temp2 = None
                # creating the images
                if each == 'rotated':
                    temp2 = df.rotate(temp, -90)[0]
                    
                elif each == 'sticker':
                    temp2 = df.strokeImage(temp, 4, background)

                elif each == 'rotatedSticker':
                    temp2 = df.rotate(df.strokeImage(temp, 4, background), -90)[0]

                elif each == 'squared':
                    temp3 = df.cropToRealSize(temp)[0]
                    exp = int(min(temp.size) * 30 / 100)
                    temp2 = df.backgroundPNG(*[each + exp for each in temp3.size], background)[0]
                    temp2 = df.pasteItem(temp2, temp3, *[temp2.size[i]//2-temp3.size[i]//2 for i in range(2)])

                
                if temp2 != None:
                    temp2.save(f'{path}\\{each}.png', optimize=True)
            
    def makePin(self):
        image2 = df.openImage(self.images['normal'])[0]
        image = df.backgroundPNG(1000, 1500, self.filebackground)
        image = df.resizeToFitSpace(image2, [each*0.95 for each in image.size])
        image = df.pasteItem(image2, image, *df.centerItem(image2, image)).convert('RGB')
        path = os.getcwd() + "\\" + "pin.jpg"
        image.save(path, optimize=True)
        self.social = path

    def delete(self):
        # removing all the images excluding normal
        for each in list(self.images.values())[1:]:
            if each is not None:
                try:
                    os.remove(each)
                except:
                    print(f"Couldn't remove {each}")