from random import uniform
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import sitedata
from playsound import playsound


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
        chrome_options.add_argument("--disable-site-isolation-trials")
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path="C:\\chromedriver\\chromedriver.exe",
            chrome_options=chrome_options
        )

        self.driver.get(sitedata.site['redbubble'])
        if (self.driver.current_url == sitedata.site['homepage1'] or
            self.driver.current_url == sitedata.site['homepage2'] ):
            self.redbubbleLogged = True
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
        if self.driver.current_url in "https://www.redbubble.com/explore/for-you/#":
            self.redbubbleLogged = True
        else:
            self.redbubbleLogged = False
            raise Exception
            
    def quit(self):
        self.driver.quit()

    def listCommands(self, file):
        find = lambda x : self.driver.find_element(By.XPATH, sitedata.site[x])
        find2 = lambda x : self.driver.find_element(By.XPATH, x)

        self.get_site = [
            lambda : self.driver.get(sitedata.site['portfolio']),
            lambda : sleep(5),
        ]

        self.get_copy = []

        if file.copyFrom != '':
            self.get_copy = [
                lambda : find('copyFrom').send_keys(file.copyFrom),
                lambda : sleep(uniform(3, 5)),
                lambda : find('copyFrom').send_keys(Keys.RETURN),
                lambda : sleep(uniform(3, 5)),
            ]

        self.get_copy += [
            lambda : find('settings').click(),
            lambda : sleep(3),
            lambda : find('copySettings').click(),
            lambda : sleep(5),
        ]
        
        self.fill_entries = [
            lambda : find('replaceImage').send_keys(file.images['normal']),
            lambda : sleep(uniform(10, 20)),
            lambda : find('openColor').click(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('sendColor').clear(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('sendColor').send_keys(file.background),
            lambda : sleep(uniform(2, 5)),
            lambda : find('title').clear(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('title').send_keys(file.title),
            lambda : sleep(uniform(2, 5)),
            lambda : find('tags').clear(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('tags').send_keys(file.tags),
            lambda : sleep(uniform(2, 5)),
            lambda : find('desc').clear(),
            lambda : sleep(uniform(2, 5)),
            lambda : find('desc').send_keys(file.desc),
            lambda : sleep(uniform(2, 5)),
        ]

        self.modify = [
            lambda x: find2(x).click(),
            lambda : sleep(uniform(3, 5)),
            lambda x, y: find2(x).send_keys(y),
            lambda : sleep(uniform(5, 9)),
        ]

        self.complete = [
            lambda : find('rights').click(),
            lambda : sleep(uniform(20, 30)),
            lambda : find('saveWork').click()
        ]
     
    def copy_thread(self, file, status, _stop):
        def wait():
            status.wait()
            _stop.wait()
        
        self.listCommands(file)
        
        for each in self.get_site:
            wait()
            each()

        for each in self.get_copy:
            wait()
            each()

        for each in self.fill_entries:
            wait()
            each()

        file.makeVariations()

        for each in file.products.keys():
            if file.products[each]['enabled']:
                wait()
                self.modify[0](sitedata.products[each][0])
                wait()
                self.modify[1]()
                wait()
                self.modify[2](sitedata.products[each][1], file.images[file.products[each]['type']])
                wait()
                self.modify[3]()
        
        for each in self.complete:
            wait()
            each()

        i = 0 
        while 'portfolio' in self.driver.current_url:
            if i > 0:
                playsound('./sounds/ka-ching.mp3')
            sleep(10)
            i += 1
    
    def pinLoginCookie(self, username, password):
        self.driver.execute_script("window.open('{}');".format(sitedata.pinData['pin_builder']))

        if self.driver.current_url == sitedata.pinData['pinterest_home']:
            self.pinterestLogged = False
            self.pinLogin(username, password)
        else:
            self.pinterestLogged = True


    def pinLogin(self, username, password):
        # Click log in link
        self.driver.find_element(By.XPATH, sitedata.pinData['pre_login_button']).click()
        # Log in
        try:
            # In case username is logged without password
            self.driver.find_element(By.NAME, "id").send_keys(username)
            sleep(uniform(2, 6))
        except:
            pass

        self.driver.find_element(By.NAME, "password").send_keys(password)
        sleep(uniform(2, 6))
        self.driver.find_element(By.XPATH, sitedata.pinData['login_button']).click()
        sleep(uniform(2, 6))

        # Checking if login has been successful
        self.driver.get(sitedata.pinData['pin_builder'])
        if self.driver.current_url == sitedata.pinData['pin_builder']:
            self.logged = True
            return
        else:
            raise Exception

    def pin(self, file):
        link = self.driver.current_url
        link = self.makeLink(link)
        publish = True
        if len(self.driver.window_handles) == 1:
            self.pinLoginCookie(None, None)
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        # Go pin builder page
        self.driver.get(sitedata.pinData["pin_builder"])
        
        file.makePin()
        
        # TODO parse link for ap page        
        sleep(uniform(2, 6))

        # Upload image
        self.driver.find_element(By.XPATH, sitedata.pinData["image_input"]).send_keys(file.social)
        sleep(uniform(2, 6))

        # Enter pin name
        if file.title:
            self.driver.find_element(By.XPATH, sitedata.pinData["pin_name"]).send_keys(file.title)
            sleep(uniform(2, 6))

        # Enter description
        if file.desc:
            self.driver.find_element(By.XPATH, sitedata.pinData["pin_description"]).send_keys(file.desc)
            sleep(uniform(2, 6))

        # Enter link
        if link:
            self.driver.find_element(By.XPATH, sitedata.pinData["pin_link"]).send_keys(link)
            sleep(uniform(2, 6))

        # Open board drop-down menu
        self.driver.find_element(By.XPATH, sitedata.pinData["drop_down_menu"]).click()
        sleep(uniform(2, 6))

        # Select board
        board = "//div[@data-test-id='board-row-" + file.board + "']"
        self.driver.find_element(By.XPATH, board).click()
        sleep(uniform(2, 6))

        if file.section:
            section = "//div[@data-test-id='section-row-" + file.section + "']"
            self.driver.find_element(By.XPATH, section).click()
            sleep(uniform(2, 6))

        elif file.section is None:
            # If section is not defined but the board is divided by section
            try:
                self.driver.find_element(By.XPATH, sitedata.pinData["section_not_defined"]).click()
                sleep(uniform(2, 6))
            except:
                pass
            
        if publish:
            # Click publish 
            self.driver.find_element(By.XPATH, sitedata.pinData["publish_button"]).click()
            sleep(uniform(7, 15))
            
                    
        else:
            # Create new pin to publish
            self.driver.find_element(By.XPATH, sitedata.pinData["new_pin"]).click()
        
        # Back to redbubble tab
        self.driver.switch_to.window(self.driver.window_handles[0])


    def makeLink(self, link):
        if link.rfind('?') != -1:
            number = link[link.rfind("/")+1:link.rfind('?')]
        else:
            number = link[link.rfind("/")+1:]

        link = "https://www.redbubble.com/shop/ap/" + number#+ "?asc=u"
        return link
