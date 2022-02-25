import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from random import uniform


# This should work until pinterest doesn't change his layout
# or html code. If any of find_element* methods doesn't work
# prepare for trouble and make it double 
# You'll need to change one of this strings
# or `board` inside pin method



class pinBot:
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
        self.driver.get(pinterest_home)
        if self.driver.current_url == pinterest_home:
            self.logged = False
            self.login()
        else:
            self.logged = True
            return

    def login(self):

            pass
        
    def pinPage(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(pin_builder)
        
    def pin(self, image, board, 
            section=None,
            title=None,
            description=None,
            link=None, 
            publish=False):
        """
        image: str, path to image
        board: str, case sensitive
        section: str (None if doesn't apply), case sensitive
        title: str
        description: str
        link: str
        publish: bool, if True pin will be published
            the reason for this is that you can create
            multiple pins in one pin builder page and
            publish them later on
               
        """

        
