import gui

driver = gui.login()

gui.work(driver=driver)

try:
    driver.quit()
except:
    pass
