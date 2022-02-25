import gui
import redbubbleCopyWork as rcw

driver = rcw.bot(None, None)

gui.work(driver=driver)

try:
    driver.quit()
except:
    pass
