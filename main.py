import gui
import redbubbleCopyWork as rcw

driver = rcw.bot()

gui.work(driver=driver)

try:
    driver.quit()
except:
    pass
