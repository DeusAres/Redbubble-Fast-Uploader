import os
from random import uniform
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import drawerFunctions as df
import sitedata


class bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.loginCookie()
 
    def loginCookie(self):
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:\\chromedriver")
        chrome_options.add_argument("profile-directory=Profile 2")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(
            executable_path="C:\\chromedriver\\chromedriver.exe",
            chrome_options=chrome_options
        )

        self.driver.get(sitedata.site['redbubble'])
        if (self.driver.current_url == sitedata.site['homepage1'] or
            self.driver.current_url == sitedata.site['homepage2'] ):
            self.logged = True
            return

        else:
            self.login()

    def login(self):
        self.driver.get("https://www.redbubble.com/auth/login")
        sleep(uniform(5, 10))
        self.driver.find_element(By.XPATH, "//input[@id='ReduxFormInput1']").send_keys(self.username)
        sleep(uniform(5, 10))
        self.driver.find_element(By.XPATH, "//input[@id='ReduxFormInput2']").send_keys(self.password)
        sleep(uniform(5, 10))
        self.driver.find_element(By.XPATH, "//button[@class='app-ui-components-Button-Button_button_1_MpP app-ui-components-Button-Button_primary_pyjm6 app-ui-components-Button-Button_padded_1fH5b']").click()
        sleep(10)
        if self.driver.current_url == "https://www.redbubble.com/explore/for-you/#":
            self.logged=True
        else:
            self.logged=False
            raise Exception
            
    def quit(self):
        self.driver.quit()

    def listCommands(self, file):
        find = lambda x : self.driver.find_element(By.XPATH, sitedata.site[x])
        find2 = lambda x : self.driver.find_element(By.XPATH, x)

        self.get_site = [
            lambda : self.driver.get(sitedata.site['portfolio']),
            lambda : sleep(3),
            lambda : find('settings').click(),
            lambda : sleep(1),
            lambda : find('copySettings').click(),
            lambda : sleep(5),
        ]
        
        self.fill_entries = [
            lambda : find('replaceImage').send_keys(file.images['normal']),
            lambda : sleep(10),
            lambda : find('openColor').click(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('sendColor').clear(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('sendColor').send_keys(file.background),
            lambda : sleep(2),
            lambda : find('title').clear(),
            lambda : sleep(2),
            lambda : find('title').send_keys(file.title),
            lambda : sleep(2),
            lambda : find('tags').clear(),
            lambda : sleep(2),
            lambda : find('tags').send_keys(file.tags),
            lambda : sleep(2),
            lambda : find('desc').clear(),
            lambda : sleep(2),
            lambda : find('desc').send_keys(file.desc),
            lambda : sleep(2),
        ]

        self.modify = [
            lambda x: find2(x).click(),
            lambda : sleep(uniform(2, 7)),
            lambda x, y: find2(x).send_keys(y),
            lambda : sleep(uniform(2, 7)),
        ]

        self.complete = [
            lambda : find('rights').click(),
            lambda : sleep(5),
            lambda : find('saveWork').click()
        ]
     
    def copy_thread(self, file, prods, status, _stop):
        def wait():
            status.wait()
            _stop.wait()
        
        self.listCommands(file)
        
        for each in self.get_site:
            wait()
            each()

        for each in self.fill_entries:
            wait()
            each()

        for each in prods.keys():
            if prods[each]['enabled']:
                wait()
                self.modify[0](sitedata.products[each][0])
                wait()
                self.modify[1]()
                wait()
                self.modify[2](sitedata.products[each][1], file.images[prods[each]['type']])
                wait()
                self.modify[3]()
        
        for each in self.complete:
            wait()
            each()

    def copy(self, file, prods):

        self.listCommands(file)
        
        for each in self.get_site:
            each()

        for each in self.fill_entries:
            each()

        for each in prods.keys():
            if prods[each]['enabled']:
                self.modify[0](sitedata.products[each][0])
                self.modify[1]()
                self.modify[2](sitedata.products[each][1], file.images[prods[each]['type']])
                self.modify[3]()
        
        for each in self.complete:
            each()

class file:
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
                

    
    def delete(self):
        # removing all the images excluding normal
        for each in list(self.images.values())[1:]:
            if each is not None:
                try:
                    os.remove(each)
                except:
                    print(f"Couldn't remove {each}")
