import os
from random import uniform
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import drawerFunctions as df

editButton = "//div[@data-type='@REPLACE']//div[@class='rb-button edit-product'][normalize-space()='Edit']"
oldUpload = "//div[contains(@class,'upload-button-wrapper')]//input[@id='select-image-@REPLACE']"
newUpload = "//div[contains(@class,'app-entries-uploaderPage-components-ReplaceDesign-ReplaceDesign_button_je6ss')]//input[@id='select-image-@REPLACE']"

products =  {
    "Standard Print Clothing": ["mens", "clothing", "old"],
    "Large Print Clothing" : ["large_clothing", "large_clothing", 'new'],
    "Caps" : ["cap", "cap", 'new'],
    "Chiffon Tops" : ["womens_panel_clothing", "womens_panel_clothing", 'new'],
    "Graphic T-shirt Dresses" : ["panel_dress", "panel_dress", 'new'],
    "Graphic T-shirt" : ["panel_clothing", "panel_clothing", 'new'],
    "A-Line Dresses" : ["trapeze_dress", "trapeze_dress", 'new'],
    "Stickers & Magnets" : ["sticker", "sticker", 'new'],
    "Phone Cases & Skins" : ["phone", "phone", "new"],
    "Desk Mat" : ["desk_mat", "desk_mat", 'new'],
    "Mouse Pad" : ["mouse_pad", "mouse_pad", 'new'],
    "Pillows & Totes" : ["thow_pillow", "thow_pillow", 'new'],
    "Prints, Cards & Posters" : ["print", "print", "old"],
    "Pouches, Laptop Skins & Sleeves" : ["laptop", "laptop", 'new'],
    "Duvets, Comforters & Shower Curtains" : ['duvet', 'duvet', 'new'],
    "Mugs" : ['mugs', 'mugs', 'old'],
    "Travel Mugs" : ["travel_mug", 'travel_mug', 'old'],
    "Mini Skirts" : ['pencil_skirt', 'pencil_skirt', 'new'],
    "Scarves" : ["scarf", "scarf", 'new'],
    "Tablet Cases & Skins" : ['tablet', 'tablet', 'new'],
    "Drawstring Bags" : ['drawstring_bag', 'drawstring_bag', 'new'],
    "Spiral Notebooks" : ['spiral_notebook', 'spiral_notebook', 'new'],
    "Hardcover Journals" : ['hardcover_journal', 'hardcover_journal', 'new'],
    "Cloks" : ["clock", 'clock', 'old'],
    "Art Board Prints" : ['gallery_board', 'gallery_board', 'new'],
    "Acrylic Blocks & Coasters" : ['acrylic_block', 'acrylic_block', 'new'],
    "Throw Blankets & Tapestries" : ['tapestry', 'tapestry', 'new'],
    "Bath Mats" : ['bath_mat', 'bath_mat', 'new'],
    "Water Bottles" : ['water_bottle', 'water_bottle', 'new'],
    "Wood & Canvas Mounted Prints" : ['mounted_print', 'mounted_print', 'new'],
    "Cotton Tote Bags" : ['cotton_tote_bag', 'cotton_tote_bag', 'new'],
    "Pin Buttons" : ['pin_button', 'pin_button', 'new'],
    "Masks" : ['mask', 'mask', 'new'],
    "Aprons" : ['apron', 'apron', 'new'],
    "Jigsaw Puzzles" : ['jigsaw_puzzle', 'jigsaw_puzzle', 'new'],
    "Sleeveless Tops" : ['panel_tank', 'panel_tank', 'new'],
    "Floor Pillows" : ['floor_pillow', 'floor_pillow', 'new'],
    "Phone Wallets" : ['phone_wallet', 'phone_wallet', 'new'],
    "Leggings" : ['leggings', 'leggings', 'new'],
    "Socks" : ['socks', 'socks', 'new'],
    "Backpacks" : ['backpack', 'backpack', 'new'],
    "Duffle Bags" : ['duffle_bag', 'duffle_bag', 'new'],
    "Fitted Masks" : ['fitted_mask', 'fitted_mask', 'new']
}

def rep(text, button):
    return button.replace("@REPLACE", text)

for each in products:
    products[each][0] = rep(products[each][0], editButton)
    if products[each][2] == 'old':
        upload = oldUpload
    elif products[each][2] == 'new':
        upload = newUpload

    products[each][1] = rep(products[each][1], upload)


class bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.fill_entries, self.modify, self.complete = [None]*3
        self.login()

        
    def login(self):
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:\\chromedriver")
        chrome_options.add_argument("profile-directory=Profile 2")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(
            executable_path="C:\\chromedriver\\chromedriver.exe",
            chrome_options=chrome_options
        )

        self.driver.get("https://www.redbubble.com")
        if self.driver.current_url in "https://www.redbubble.com/explore/for-you/#":
            self.logged=True
            return
        
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

    def quit(self):
        self.driver.quit()

    def listCommands(self, file):
        self.fill_entries = [
            lambda : self.driver.get("https://www.redbubble.com/portfolio/manage_works?ref=account-nav-dropdown"),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//div[@class='works']//div[1]//div[1]//div[1]").click(),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//div[@class='works']//div[1]//div[1]//div[2]//a[3]").click(),
            lambda : sleep(uniform(10,20)),
            lambda : self.driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/form/div/div[1]/div[1]/input').send_keys(file.images['normal']),
            lambda : sleep(uniform(10, 15)),
            lambda : self.driver.find_element(By.XPATH, "//input[@id='work_title_en']").clear(),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//input[@id='work_title_en']").send_keys(file.title),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//textarea[@id='work_tag_field_en']").clear(),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//textarea[@id='work_tag_field_en']").send_keys(file.tags),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//textarea[@id='work_description_en']").clear(),
            lambda : sleep(uniform(5,10)),
            lambda : self.driver.find_element(By.XPATH, "//textarea[@id='work_description_en']").send_keys(file.description),
            lambda : sleep(uniform(5,10)),
        ]
        self.modify = [
            lambda x: self.driver.find_element(By.XPATH, x).click(),
            lambda : sleep(uniform(5, 10)),
            lambda x, y: self.driver.find_element(By.XPATH, x).send_keys(y),
            lambda : sleep(uniform(10, 25))
        ]
        self.complete = [
            lambda : self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END),
            #lambda : self.driver.find_element(By.XPATH, "//input[@id='work_safe_for_work_True']").click(),
            lambda : self.driver.find_element(By.XPATH, "//input[@id='rightsDeclaration']").click(),
            lambda : self.driver.find_element(By.XPATH, "//input[@id='submit-work']").click(),
        ]
     
    def copy_thread(self, file, prods, status, _stop):

        def wait():
            status.wait()
            _stop.wait()
        
        if all(each == None for each in [self.modify, self.complete, self.fill_entries]):
            self.listCommands(file)

        for each in self.fill_entries:
            each()
            wait()

        for each in prods.keys():
            if prods[each]['enabled']:
                self.modify[0](products[each][0])
                wait()
                self.modify[1]()
                wait()
                self.modify[2](products[each][1], file.images[prods[each]['type']])
                wait()
                self.modify[3]()
                wait()
        
        for each in self.complete:
            each()
            wait()

    def copy(self, file, prods):

        if all(each == None for each in [self.modify, self.complete, self.fill_entries]):
            self.listCommands(file)

        for each in self.fill_entries:
            each()

        for each in prods.keys():
            if prods[each]['enabled']:
                self.modify[0](products[each][0])
                self.modify[1]()
                self.modify[2](products[each][1], file.images[prods[each]['type']])
                self.modify[3]()
        
        for each in self.complete:
            each()

class file:
    def __init__(self, image, title, tags, description, types):
        self.title = title
        self.tags = tags
        self.description = description
        self.images = {
            'normal' : image,
            'rotated' : None,
            'sticker' : None,
            'rotatedSticker' : None
        }

        temp = df.openImage(image)[0].convert("RGBA")
        for each in types:
            path = os.getcwd()
            # saving the path
            if each in self.images.keys() and each != 'normal':
                self.images[each] = f'{path}\\{each}.png'

                # creating the images
                if each == 'rotated':
                    temp2 = df.rotate(temp, -90)[0].save(f'.\\{each}.png', optimize=True)
                    
                elif each == 'sticker':
                    temp2 = df.strokeImage(temp, 4, '#000000').save(f'.\\{each}.png', optimize=True)

                elif each == 'rotatedSticker':
                    temp2 = df.rotate(df.strokeImage(temp, 4, '#000000'), -90)[0]

                try:
                    temp2.save(f'{path}\\{each}.png', optimize=True)
                except:
                    pass
    
    def __delete__(self):
        # removing all the images excluding normal
        for each in list(self.images.values())[1:]:
            if each != None:
                try:
                    os.remove(each)
                except:
                    print(f"Couldn't remove {each}")

b = bot(None, None)
input()